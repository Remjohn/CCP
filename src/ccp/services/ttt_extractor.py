"""
CCP TTT Baseline Extractor
Task 1.10 — Extracts the coach's Voice DNA from Sacred Audio transcripts.

TTT = Tone, Texture, Timing. The baseline captures:
- Sentence rhythm (short/long patterns, question frequency)
- Metaphor patterns (animal, nature, warfare, body, etc.)
- Vocabulary fingerprint (signature words and phrases)
- Emotional peak markers (how the coach builds to key moments)
- Pause cadence (breathing patterns, emphasis through silence)
- Humor style (dry, warm, self-deprecating, absurd, etc.)

The output populates the voice_dna section of coach_soul.json.
"""

import hashlib
import json
import re
from collections import Counter
from typing import Optional

from src.ccp.models.coach_soul import VoiceDNA


# Metaphor family detection patterns
METAPHOR_FAMILIES = {
    "animal": [
        r"\blion\b", r"\bwolf\b", r"\beagle\b", r"\bsnake\b", r"\bbear\b",
        r"\bbutterfly\b", r"\bphoenix\b", r"\bhawk\b", r"\bsheep\b", r"\bprey\b",
        r"\bpredator\b", r"\bhunt\b", r"\bpack\b", r"\bwild\b", r"\bcage\b",
    ],
    "nature": [
        r"\bseed\b", r"\broot\b", r"\bgrow\b", r"\bbloom\b", r"\bstorm\b",
        r"\bfire\b", r"\bwater\b", r"\bocean\b", r"\bmountain\b", r"\bforest\b",
        r"\bseason\b", r"\bwinter\b", r"\bspring\b", r"\bharvest\b", r"\bsoil\b",
    ],
    "warfare": [
        r"\bbattle\b", r"\bfight\b", r"\bwarrior\b", r"\bshield\b", r"\bsword\b",
        r"\barmor\b", r"\bdefend\b", r"\bsurrender\b", r"\bvictory\b", r"\bconquer\b",
    ],
    "body": [
        r"\bheart\b", r"\bgut\b", r"\bbone\b", r"\bbreath\b", r"\bspine\b",
        r"\bshoulder\b", r"\bblood\b", r"\bskin\b", r"\bfist\b", r"\bchest\b",
    ],
    "light_dark": [
        r"\blight\b", r"\bdark\b", r"\bshadow\b", r"\bshine\b", r"\bflame\b",
        r"\bspark\b", r"\beclipse\b", r"\bdawn\b", r"\bdusk\b", r"\bglow\b",
    ],
    "journey": [
        r"\bpath\b", r"\broad\b", r"\bstep\b", r"\bwalk\b", r"\bjourney\b",
        r"\bdoor\b", r"\bbridge\b", r"\bcrossroad\b", r"\bdestination\b", r"\bmap\b",
    ],
    "mirror": [
        r"\bmirror\b", r"\breflect\b", r"\bsee yourself\b", r"\blook at\b",
        r"\brecognize\b", r"\bface\b", r"\btruth\b", r"\bunmask\b",
    ],
}

# Emotional intensity markers
PEAK_PATTERNS = [
    r"(?:\.{3}|—)\s+[A-Z]",           # Pause before emphasis (... Then / — But)
    r"\b(?:actually|really|truly)\b",   # Intensifier words
    r"[.!?]\s+And\b",                  # "And" as sentence starter (dramatic continuation)
    r"\b(?:listen|look|here's the thing)\b",  # Direct address pivots
    r"[.]\s+[A-Z][a-z]+\.\s*$",        # Short final sentence (mic drop)
]

# Humor style indicators
HUMOR_MARKERS = {
    "self_deprecating": [r"\bI used to\b", r"\bmy mistake\b", r"\bI was wrong\b", r"\bI'm the worst\b"],
    "ironic": [r"\bof course\b", r"\bobviously\b", r"\bsurprise surprise\b", r"\bimagine that\b"],
    "absurd": [r"\bimagine\b.*\b(?:elephant|unicorn|alien|zombie)\b"],
    "dry": [r"\bthat's it\b", r"\bthat's all\b", r"\bmoving on\b", r"\banyway\b"],
    "warm": [r"\bI love\b", r"\bmy favorite\b", r"\bit's beautiful\b", r"\bhonestly\b"],
}


class TTTExtractor:
    """Extract Voice DNA (Tone, Texture, Timing) from transcribed audio."""

    def __init__(self):
        self._metaphor_patterns = {
            family: [re.compile(p, re.IGNORECASE) for p in patterns]
            for family, patterns in METAPHOR_FAMILIES.items()
        }
        self._peak_patterns = [re.compile(p, re.MULTILINE) for p in PEAK_PATTERNS]
        self._humor_patterns = {
            style: [re.compile(p, re.IGNORECASE) for p in markers]
            for style, markers in HUMOR_MARKERS.items()
        }

    def extract(self, transcripts: list[str]) -> VoiceDNA:
        """Extract Voice DNA from one or more Sacred Audio transcripts.

        Args:
            transcripts: List of transcription text strings

        Returns:
            VoiceDNA model populated with extracted patterns
        """
        full_text = "\n\n".join(transcripts)
        sentences = self._split_sentences(full_text)

        return VoiceDNA(
            sentence_rhythm=self._analyze_rhythm(sentences),
            metaphor_patterns=self._detect_metaphors(full_text),
            vocabulary_fingerprint=self._extract_vocabulary(full_text),
            emotional_peak_markers=self._detect_peaks(full_text),
            pause_cadence=self._analyze_pauses(full_text),
            humor_style=self._detect_humor_style(full_text),
            ttt_baseline_hash=self._compute_hash(full_text),
        )

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _analyze_rhythm(self, sentences: list[str]) -> list[str]:
        """Analyze sentence length patterns and rhythm."""
        if not sentences:
            return ["insufficient_data"]

        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        short_ratio = sum(1 for l in lengths if l <= 5) / len(lengths)
        long_ratio = sum(1 for l in lengths if l >= 20) / len(lengths)
        question_ratio = sum(1 for s in sentences if s.endswith("?")) / len(lengths)

        patterns = []

        # Rhythm classification
        if short_ratio > 0.4:
            patterns.append("punchy_short_sentences")
        if long_ratio > 0.3:
            patterns.append("flowing_long_form")
        if avg_length < 10:
            patterns.append("concise_communicator")
        elif avg_length > 18:
            patterns.append("expansive_storyteller")
        else:
            patterns.append("balanced_rhythm")

        if question_ratio > 0.15:
            patterns.append("frequent_questioner")
        if question_ratio > 0.25:
            patterns.append("socratic_style")

        # Check for short-long alternation (dramatic effect)
        alternations = 0
        for i in range(1, len(lengths)):
            if (lengths[i-1] <= 6 and lengths[i] >= 15) or (lengths[i-1] >= 15 and lengths[i] <= 6):
                alternations += 1
        if alternations / max(len(lengths) - 1, 1) > 0.2:
            patterns.append("dramatic_alternation")

        return patterns

    def _detect_metaphors(self, text: str) -> list[str]:
        """Detect dominant metaphor families."""
        family_counts: dict[str, int] = {}
        for family, patterns in self._metaphor_patterns.items():
            count = sum(len(p.findall(text)) for p in patterns)
            if count > 0:
                family_counts[family] = count

        # Return families sorted by frequency, with count annotations
        sorted_families = sorted(family_counts.items(), key=lambda x: x[1], reverse=True)
        return [f"{family}({count})" for family, count in sorted_families if count >= 2]

    def _extract_vocabulary(self, text: str) -> list[str]:
        """Extract signature vocabulary — words used significantly more than average."""
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        counter = Counter(words)

        # Filter out common words (stopword-like)
        common_words = {
            "that", "this", "with", "have", "from", "they", "been", "were",
            "will", "would", "could", "should", "about", "their", "which",
            "when", "what", "your", "just", "like", "know", "think", "going",
            "want", "because", "really", "something", "thing", "things",
            "people", "person", "time", "make", "very", "some", "into",
            "them", "then", "than", "more", "also", "here", "there",
        }

        # Get words that appear 3+ times and aren't common
        total_words = len(words)
        significant = []
        for word, count in counter.most_common(50):
            if word not in common_words and count >= 3:
                freq = count / total_words
                if freq > 0.002:  # More than 0.2% of all words
                    significant.append(word)

        return significant[:20]  # Top 20 signature words

    def _detect_peaks(self, text: str) -> list[str]:
        """Detect emotional peak building patterns."""
        markers = []
        for i, pattern in enumerate(self._peak_patterns):
            matches = pattern.findall(text)
            if len(matches) >= 2:
                labels = [
                    "pause_then_emphasis",
                    "intensifier_words",
                    "dramatic_and_continuation",
                    "direct_address_pivot",
                    "mic_drop_closer",
                ]
                if i < len(labels):
                    markers.append(f"{labels[i]}({len(matches)})")

        return markers if markers else ["subtle_builder"]

    def _analyze_pauses(self, text: str) -> str:
        """Analyze pause/breathing patterns from punctuation."""
        ellipsis_count = text.count("...")
        dash_count = text.count("—") + text.count(" - ")
        comma_rate = text.count(",") / max(len(text.split()), 1)

        if ellipsis_count > 5:
            return "reflective_pauser"
        elif dash_count > 5:
            return "dynamic_interrupter"
        elif comma_rate > 0.15:
            return "flowing_connector"
        else:
            return "direct_speaker"

    def _detect_humor_style(self, text: str) -> Optional[str]:
        """Detect dominant humor style from markers."""
        style_counts: dict[str, int] = {}
        for style, patterns in self._humor_patterns.items():
            count = sum(len(p.findall(text)) for p in patterns)
            if count > 0:
                style_counts[style] = count

        if not style_counts:
            return None

        dominant = max(style_counts, key=style_counts.get)
        return dominant

    @staticmethod
    def _compute_hash(text: str) -> str:
        """Compute a hash of the full text for drift detection baseline."""
        return hashlib.sha256(text.encode()).hexdigest()[:32]
