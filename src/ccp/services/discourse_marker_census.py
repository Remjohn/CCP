"""
CCP FR3 Discourse Marker Census — Unit 3
Scans the extraction corpus for transitional glue words with position mapping.

Spec reference: FR3 Tech Spec §Step 2 — Discourse Marker Census
Agent: Valeriane + spaCy POS tagging

Action:
- Scan full corpus for: actually, so, look, right, I mean, you know, basically, literally
- Count total occurrences per marker
- Map syntactic position: sentence-opening, sentence-middle, clause-bridging
- Calculate position distribution percentages
"""

import re
from typing import Optional

from src.ccp.models.voice_dna_models import (
    DiscourseMarkerMap,
    ExtractionCorpus,
    MarkerPositionDistribution,
)


# ──────────────────────────────────────────────────────────────
# Discourse markers from spec
# Spec §Step 2: "actually, so, look, right, I mean, you know, basically, literally"
# ──────────────────────────────────────────────────────────────

DISCOURSE_MARKERS: list[str] = [
    "actually",
    "so",
    "look",
    "right",
    "i mean",
    "you know",
    "basically",
    "literally",
]

# Extended markers beyond spec minimum — common coaching discourse glue
EXTENDED_MARKERS: list[str] = [
    "honestly",
    "like",
    "well",
    "okay",
    "see",
    "now",
    "really",
    "just",
    "obviously",
    "essentially",
    "clearly",
    "frankly",
    "seriously",
    "technically",
    "naturally",
]


class DiscourseMarkerCensus:
    """Scans the extraction corpus for discourse markers with position mapping.

    Spec §Step 2: 'For each marker: count total occurrences, map their syntactic
    position: sentence-opening, sentence-middle, clause-bridging. Calculate the
    position distribution.'

    Uses spaCy for sentence splitting and syntactic position detection.
    Falls back to regex-based sentence splitting if spaCy unavailable.
    """

    def __init__(self, spacy_model=None, include_extended: bool = True):
        """Initialize with optional spaCy model.

        Args:
            spacy_model: Pre-loaded spaCy model. If None, uses regex fallback.
            include_extended: Include extended markers beyond the spec 8.
        """
        self.nlp = spacy_model
        self.markers = list(DISCOURSE_MARKERS)
        if include_extended:
            self.markers.extend(EXTENDED_MARKERS)

        # Sort by length descending so multi-word markers match first
        self.markers.sort(key=len, reverse=True)

        # Compile regex patterns for each marker
        self._marker_patterns: dict[str, re.Pattern] = {}
        for marker in self.markers:
            # Case-insensitive word boundary match
            escaped = re.escape(marker)
            self._marker_patterns[marker] = re.compile(
                rf"\b{escaped}\b", re.IGNORECASE
            )

    def census(self, corpus: ExtractionCorpus) -> DiscourseMarkerMap:
        """Execute Step 2: Discourse Marker Census.

        Args:
            corpus: Assembled extraction corpus from Step 1.

        Returns:
            DiscourseMarkerMap with all marker position distributions.
        """
        # Concatenate all unit texts
        full_text = " ".join(u.text for u in corpus.units)

        # Split into sentences
        sentences = self._split_sentences(full_text)

        # Initialize result
        result = DiscourseMarkerMap(corpus_hash=corpus.corpus_hash)

        for marker in self.markers:
            distribution = self._analyze_marker(marker, sentences)
            if distribution.total_occurrences > 0:
                result.markers[marker] = distribution

        return result

    def census_for_cluster(
        self, units_text: str
    ) -> dict[str, MarkerPositionDistribution]:
        """Run census on a subset of text (for cross-topic invariance).

        Args:
            units_text: Concatenated text for a single topic cluster.

        Returns:
            Dict of marker → MarkerPositionDistribution.
        """
        sentences = self._split_sentences(units_text)
        distributions: dict[str, MarkerPositionDistribution] = {}

        for marker in self.markers:
            dist = self._analyze_marker(marker, sentences)
            if dist.total_occurrences > 0:
                distributions[marker] = dist

        return distributions

    def _analyze_marker(
        self, marker: str, sentences: list[str]
    ) -> MarkerPositionDistribution:
        """Analyze a single marker's occurrences and positions across sentences.

        Position classification:
        - Sentence-opening: marker appears in first 3 words of sentence
        - Clause-bridging: marker appears after a comma or semicolon
        - Sentence-middle: all other positions
        """
        dist = MarkerPositionDistribution(marker=marker)
        pattern = self._marker_patterns[marker]

        for sentence in sentences:
            sentence_stripped = sentence.strip()
            if not sentence_stripped:
                continue

            words = sentence_stripped.split()
            if not words:
                continue

            matches = list(pattern.finditer(sentence_stripped))
            for match in matches:
                dist.total_occurrences += 1
                position = match.start()

                # Classify position
                if self._is_sentence_opening(sentence_stripped, position, marker):
                    dist.sentence_opening_count += 1
                elif self._is_clause_bridging(sentence_stripped, position):
                    dist.clause_bridging_count += 1
                else:
                    dist.sentence_middle_count += 1

        dist.compute_percentages()
        return dist

    def _is_sentence_opening(
        self, sentence: str, position: int, marker: str
    ) -> bool:
        """Check if marker is at sentence opening (first 3 words).

        Spec §Step 2: 'sentence-opening' position category.
        """
        # Get text before the marker
        prefix = sentence[:position].strip()
        # If nothing before marker, or only 1-2 words, it's sentence-opening
        if not prefix:
            return True
        prefix_words = prefix.split()
        return len(prefix_words) <= 2

    def _is_clause_bridging(self, sentence: str, position: int) -> bool:
        """Check if marker follows a comma, semicolon, or dash.

        Spec §Step 2: 'clause-bridging' position category.
        """
        # Look at character just before the marker position
        for i in range(position - 1, max(position - 4, -1), -1):
            if i < 0:
                return False
            char = sentence[i]
            if char in {",", ";", "—", "-", ":"}:
                return True
            if char == " ":
                continue
            break
        return False

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences using spaCy or regex fallback."""
        if self.nlp is not None:
            doc = self.nlp(text)
            return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        # Regex fallback: split on sentence-ending punctuation
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]
