"""
CCP Thought Unit Segmentation — FR2 Unit 3
spaCy-based syntactic dependency parsing for logic-driven chunking.

Spec reference: FR2 Tech Spec §Stage C — Thought Unit Segmentation

Principle: Voice DNA Framework Principal 1 — logic-driven chunking.
A Thought_Unit is a complete logical move: [claim → mechanism → emotional assertion].
Token limits are irrelevant. Timestamp boundaries are irrelevant.

Segmentation Rules (from spec):
1. Parse transcript via spaCy dependency tree
2. A segment boundary is drawn ONLY when:
   - A complete logical move resolves, AND
   - The dependency tree returns to a root state, AND
   - A natural pause marker (≥500ms silence or filler-pause sequence) is detected
3. Segments shorter than 30 words are merged with the subsequent segment
4. Edge case: >500 words without root return → force-segment at 300-word mark
5. Edge case: Multilingual code-switching → flag for manual review
"""

import re
import uuid
from typing import Any, Optional

from src.ccp.models.sacred_audio_models import ThoughtUnit

# Minimum word count for a valid thought unit (spec: "Segments shorter than
# 30 words are merged with the subsequent segment")
MIN_SEGMENT_WORDS: int = 30

# Force-segment threshold (spec: "Long continuous streams >500 words without
# a root return: force-segment at the 300-word mark")
FORCE_SEGMENT_WORDS: int = 300

# Maximum words before a force-segment is triggered
MAX_WORDS_WITHOUT_ROOT: int = 500

# Pause threshold in milliseconds (spec: "≥500ms silence")
PAUSE_THRESHOLD_MS: float = 500.0


def _detect_pause_at_position(
    word_idx: int,
    timestamps: list[dict[str, Any]],
) -> bool:
    """Check if there's a ≥500ms pause after word at word_idx.

    Spec: 'A natural pause marker (≥500ms silence from Whisper timestamps,
    or filler-pause sequence) is detected.'

    Args:
        word_idx: Index of the current word in the transcript
        timestamps: Word-level timestamps from Whisper

    Returns:
        True if a ≥500ms pause is detected after this word.
    """
    if not timestamps or word_idx >= len(timestamps) - 1:
        return False

    current = timestamps[word_idx]
    next_word = timestamps[word_idx + 1]

    current_end = current.get("end", 0.0)
    next_start = next_word.get("start", 0.0)

    gap_ms = (next_start - current_end) * 1000  # Convert seconds to ms
    return gap_ms >= PAUSE_THRESHOLD_MS


def _detect_multilingual(text: str) -> bool:
    """Detect potential multilingual code-switching.

    Spec: 'Multilingual code-switching: flag for manual review —
    do not segment cross-language units.'

    Simple heuristic: checks for non-Latin script characters that
    suggest language switching.
    """
    # Check for CJK, Cyrillic, Arabic, Devanagari, etc.
    non_latin_pattern = re.compile(
        r'[\u0400-\u04FF'   # Cyrillic
        r'\u0600-\u06FF'    # Arabic
        r'\u0900-\u097F'    # Devanagari
        r'\u3040-\u309F'    # Hiragana
        r'\u30A0-\u30FF'    # Katakana
        r'\u4E00-\u9FFF'    # CJK
        r'\uAC00-\uD7AF]'   # Korean
    )
    return bool(non_latin_pattern.search(text))


class ThoughtUnitSegmenter:
    """Segments raw transcripts into logic-bounded Thought Units using spaCy.

    Spec: 'Engine: Pi Coding Agent + spaCy (en_core_web_sm or equivalent)
    for syntactic dependency parsing.'
    """

    def __init__(self, spacy_model: Optional[Any] = None):
        """Initialize with a spaCy language model.

        Args:
            spacy_model: Pre-loaded spaCy model. If None, loads en_core_web_sm.
        """
        if spacy_model is not None:
            self.nlp = spacy_model
        else:
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
            except (ImportError, OSError):
                raise RuntimeError(
                    "spaCy model 'en_core_web_sm' not available. "
                    "Install with: python -m spacy download en_core_web_sm"
                )

    def segment(
        self,
        transcript: str,
        whisper_timestamps: Optional[list[dict[str, Any]]] = None,
        session_id: str = "",
    ) -> list[ThoughtUnit]:
        """Segment a transcript into Thought Units.

        Spec §Stage C Segmentation Rules:
        1. Parse transcript via spaCy dependency tree
        2. Boundary drawn only when logical move resolves + root state + pause
        3. Segments shorter than 30 words merged with subsequent segment
        4. >500 words → force-segment at 300

        Args:
            transcript: Raw transcript text (with non-verbals preserved)
            whisper_timestamps: Word-level timestamps from Whisper
            session_id: Session identifier for unit ID generation

        Returns:
            List of ThoughtUnit objects
        """
        if not transcript.strip():
            return []

        timestamps = whisper_timestamps or []

        # Check for multilingual content
        is_multilingual = _detect_multilingual(transcript)

        # Parse with spaCy
        doc = self.nlp(transcript)

        # Find segment boundaries
        raw_segments = self._find_boundaries(doc, timestamps)

        # Merge short segments (< 30 words)
        merged_segments = self._merge_short_segments(raw_segments)

        # Convert to ThoughtUnit objects
        units = []
        for idx, segment_data in enumerate(merged_segments):
            unit_id = f"TU-{session_id}-{idx + 1:03d}" if session_id else f"TU-{uuid.uuid4().hex[:8]}-{idx + 1:03d}"
            text = segment_data["text"]
            word_count = len(text.split())

            # Extract relevant timestamps for this segment
            segment_timestamps = self._extract_timestamps(
                segment_data["start_word_idx"],
                segment_data["end_word_idx"],
                timestamps,
            )

            units.append(ThoughtUnit(
                unit_id=unit_id,
                text=text,
                word_count=word_count,
                whisper_timestamps=segment_timestamps,
                hard_boundary=segment_data.get("hard_boundary", False),
                multilingual_flag=is_multilingual,
            ))

        return units

    def _find_boundaries(
        self,
        doc: Any,
        timestamps: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Find segment boundaries using spaCy dependency tree.

        Spec: 'A segment boundary is drawn ONLY when:
        - A complete logical move (claim + mechanism + emotional assertion) resolves, AND
        - The dependency tree returns to a root state (no open subordinate clauses), AND
        - A natural pause marker (≥500ms silence or filler-pause sequence) is detected'

        Returns:
            List of segment dicts with text, start/end word indices, and flags.
        """
        segments: list[dict[str, Any]] = []
        current_segment_words: list[str] = []
        current_start_idx: int = 0
        words_since_last_boundary: int = 0
        word_idx: int = 0

        for sent in doc.sents:
            for token in sent:
                current_segment_words.append(token.text_with_ws)
                words_since_last_boundary += 1
                word_idx += 1

                # Force-segment check (spec edge case)
                # "Long continuous streams (>500 words without a root return):
                # force-segment at the 300-word mark"
                if words_since_last_boundary >= FORCE_SEGMENT_WORDS:
                    text = "".join(current_segment_words).strip()
                    if text:
                        segments.append({
                            "text": text,
                            "start_word_idx": current_start_idx,
                            "end_word_idx": word_idx - 1,
                            "hard_boundary": True,
                        })
                    current_segment_words = []
                    current_start_idx = word_idx
                    words_since_last_boundary = 0
                    continue

                # Check for root state: token.dep_ == "ROOT" means the
                # dependency tree has returned to root level
                is_root_return = token.dep_ == "ROOT" or (
                    token.dep_ in ("punct", "cc") and
                    token.head.dep_ == "ROOT"
                )

                # Check if we're at end of a sentence (complete logical move)
                is_sentence_end = token.is_sent_end or (
                    token.text in ".!?" and token.i == sent.end - 1
                )

                # Check for pause marker
                has_pause = _detect_pause_at_position(word_idx - 1, timestamps)

                # Filler-pause sequence detection
                is_filler = token.text.lower().strip() in {"um", "uh", "hmm", "uhh", "umm"}

                # Boundary condition: root return + (sentence end OR pause OR filler-pause)
                if (is_root_return or is_sentence_end) and (
                    has_pause or is_sentence_end or is_filler
                ):
                    text = "".join(current_segment_words).strip()
                    if text:
                        segments.append({
                            "text": text,
                            "start_word_idx": current_start_idx,
                            "end_word_idx": word_idx - 1,
                            "hard_boundary": False,
                        })
                    current_segment_words = []
                    current_start_idx = word_idx
                    words_since_last_boundary = 0

        # Don't lose trailing text
        remaining = "".join(current_segment_words).strip()
        if remaining:
            segments.append({
                "text": remaining,
                "start_word_idx": current_start_idx,
                "end_word_idx": word_idx - 1,
                "hard_boundary": False,
            })

        return segments

    def _merge_short_segments(
        self,
        segments: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Merge segments shorter than 30 words with the subsequent segment.

        Spec: 'Segments shorter than 30 words are merged with the
        subsequent segment (too short for LIWC-22 scoring).'
        """
        if not segments:
            return []

        merged: list[dict[str, Any]] = []
        carry_over: Optional[dict[str, Any]] = None

        for segment in segments:
            if carry_over is not None:
                # Merge carry_over into this segment
                segment = {
                    "text": carry_over["text"] + " " + segment["text"],
                    "start_word_idx": carry_over["start_word_idx"],
                    "end_word_idx": segment["end_word_idx"],
                    "hard_boundary": segment.get("hard_boundary", False),
                }
                carry_over = None

            word_count = len(segment["text"].split())
            if word_count < MIN_SEGMENT_WORDS:
                carry_over = segment
            else:
                merged.append(segment)

        # If the last segment was too short, merge it with the previous one
        if carry_over is not None:
            if merged:
                last = merged[-1]
                merged[-1] = {
                    "text": last["text"] + " " + carry_over["text"],
                    "start_word_idx": last["start_word_idx"],
                    "end_word_idx": carry_over["end_word_idx"],
                    "hard_boundary": last.get("hard_boundary", False),
                }
            else:
                # Only segment and it's short — still include it
                merged.append(carry_over)

        return merged

    def _extract_timestamps(
        self,
        start_idx: int,
        end_idx: int,
        timestamps: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Extract word-level timestamps for a segment range."""
        if not timestamps:
            return []
        return timestamps[start_idx:end_idx + 1]
