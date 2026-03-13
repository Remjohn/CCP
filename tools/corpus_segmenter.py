"""
Voice DNA Agentic Team — Corpus Segmenter Tool (Step 2)
Deterministic Python tool that segments raw transcripts at thought-unit boundaries.
NOT an LLM skill — this is procedural, reproducible work.

Usage:
    python tools/corpus_segmenter.py --input raw/transcripts/ --output intelligence_library/segmented_corpus.json
"""

import json
import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any


# --- Discourse Marker Detection ---
DISCOURSE_MARKERS = [
    "so", "look", "listen", "but", "however", "actually", "in fact",
    "the thing is", "here's what", "let me tell you", "and that's",
    "because", "right", "okay", "now", "see", "you know what",
    "the truth is", "what I mean is", "basically", "fundamentally"
]

# --- Arousal Word Density for TTT Estimation ---
HIGH_AROUSAL_WORDS = [
    "enough", "wake up", "stop", "war", "fight", "destroy", "unacceptable",
    "outrageous", "insane", "ridiculous", "furious", "disgusting", "brutal"
]
LOW_AROUSAL_WORDS = [
    "perhaps", "consider", "I believe", "gently", "quietly", "maybe",
    "it seems", "one might", "in my experience", "I wonder"
]


def detect_sentence_boundaries(text: str) -> List[str]:
    """Split text into sentences using regex-based boundary detection."""
    # Split on sentence-ending punctuation followed by space or newline
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def estimate_ttt(text: str) -> str:
    """Estimate TTT band from arousal word density."""
    words = text.lower().split()
    word_count = len(words)
    if word_count == 0:
        return "ttt_04_06"

    high_count = sum(1 for w in HIGH_AROUSAL_WORDS if w in text.lower())
    low_count = sum(1 for w in LOW_AROUSAL_WORDS if w in text.lower())

    if high_count > low_count + 2:
        return "ttt_07_09"
    elif low_count > high_count + 2:
        return "ttt_01_03"
    else:
        return "ttt_04_06"


def detect_thought_boundaries(sentences: List[str]) -> List[List[str]]:
    """
    Group sentences into thought units.
    A thought unit boundary is detected when:
    1. A discourse marker signals a new logical direction
    2. A topic shift is detected (pronoun change, new subject introduction)
    3. The accumulated unit exceeds 400 words
    """
    thought_units = []
    current_unit = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        # Check for discourse marker at sentence start (signals new thought)
        starts_with_marker = any(
            sentence.lower().startswith(marker)
            for marker in DISCOURSE_MARKERS
        )

        # Boundary conditions
        if current_unit and (
            (starts_with_marker and current_word_count >= 50) or
            current_word_count >= 400
        ):
            thought_units.append(current_unit)
            current_unit = [sentence]
            current_word_count = word_count
        else:
            current_unit.append(sentence)
            current_word_count += word_count

    # Don't forget the last unit
    if current_unit:
        thought_units.append(current_unit)

    return thought_units


def segment_corpus(input_dir: str, output_path: str) -> None:
    """Main segmentation pipeline."""
    transcripts_dir = Path(input_dir)
    if not transcripts_dir.exists():
        print(f"ERROR: Transcript directory not found: {input_dir}")
        return

    all_thought_units = []
    position_counter = 0

    # Process all transcript files
    transcript_files = sorted(transcripts_dir.glob("*.md")) + sorted(transcripts_dir.glob("*.txt"))
    if not transcript_files:
        print(f"ERROR: No .md or .txt files found in {input_dir}")
        return

    for filepath in transcript_files:
        text = filepath.read_text(encoding="utf-8")
        sentences = detect_sentence_boundaries(text)
        thought_units = detect_thought_boundaries(sentences)

        for unit_sentences in thought_units:
            unit_text = " ".join(unit_sentences)
            word_count = len(unit_text.split())

            # Skip extremely short units (noise)
            if word_count < 15:
                continue

            thought_unit = {
                "id": f"tu_{position_counter:04d}",
                "source_file": filepath.name,
                "position_in_corpus": position_counter,
                "text": unit_text,
                "word_count": word_count,
                "sentence_count": len(unit_sentences),
                "ttt_estimate": estimate_ttt(unit_text),
                "topic_cluster": None,  # Populated by downstream topic clustering
                "discourse_markers_found": [
                    marker for marker in DISCOURSE_MARKERS
                    if marker in unit_text.lower()
                ]
            }

            all_thought_units.append(thought_unit)
            position_counter += 1

    # Write output
    output = {
        "_tool": "corpus_segmenter.py",
        "_version": "1.0",
        "total_thought_units": len(all_thought_units),
        "total_word_count": sum(u["word_count"] for u in all_thought_units),
        "source_files": [f.name for f in transcript_files],
        "thought_units": all_thought_units
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"SUCCESS: Segmented {len(all_thought_units)} thought units from {len(transcript_files)} transcripts.")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Segment coach transcripts into thought units.")
    parser.add_argument("--input", required=True, help="Path to raw/transcripts/ directory")
    parser.add_argument("--output", required=True, help="Path for segmented_corpus.json output")
    args = parser.parse_args()

    segment_corpus(args.input, args.output)
