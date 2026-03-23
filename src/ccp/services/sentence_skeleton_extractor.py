"""
CCP FR3 Sentence Skeleton Extraction — Unit 5
Strips content words, retains function words, and computes the 6-cluster stylometry profile.

Spec reference: FR3 Tech Spec §Step 4 — Sentence Skeleton Extraction (Stylometry Profiling)
Agent: Valeriane + spaCy dependency parser

Action:
- Strip all content nouns and verbs from each Thought Unit
- Retain only: function words, conjunctions, prepositions, determiners, pronouns, punctuation, discourse markers
- Calculate 6 cluster variable groups:
  1. Lexical/Morphological (TTR, hapax legomena frequency, vocabulary density)
  2. Subconscious Syntactic Distributions (function word ratios, clause connective patterns)
  3. Relational WAN Metrics (preposition-conjunction transition probabilities, adjacency network)
  4. Graphical Habits (punctuation density, capitalization anomalies)
  5. Structural Complexity (WPS flow, paragraph length variance)
  6. Invariant discourse markers (from Step 3)

Output: StylometryProfile (60-variable profile — core of DEP-ENG-003)
"""

import re
import statistics
from collections import Counter, defaultdict
from typing import Optional

from src.ccp.models.voice_dna_models import (
    ExtractionCorpus,
    GraphicalHabitsCluster,
    LexicalMorphologicalCluster,
    StylometryProfile,
    StructuralComplexityCluster,
    SyntacticDistributionCluster,
    WANMetricsCluster,
)


# ──────────────────────────────────────────────────────────────
# Function words to retain during skeleton extraction
# ──────────────────────────────────────────────────────────────

FUNCTION_WORDS: set[str] = {
    # Conjunctions
    "and", "but", "or", "nor", "for", "yet", "so", "because", "although",
    "though", "while", "since", "unless", "until", "if", "when", "where",
    "whereas", "however", "therefore", "moreover", "furthermore", "nevertheless",
    "nonetheless", "meanwhile", "otherwise", "hence", "thus", "consequently",
    # Prepositions
    "in", "on", "at", "to", "from", "by", "with", "without", "about",
    "through", "during", "before", "after", "between", "among", "into",
    "out", "over", "under", "above", "below", "around", "against", "across",
    "behind", "beyond", "toward", "towards", "within", "upon",
    # Determiners
    "the", "a", "an", "this", "that", "these", "those", "my", "your",
    "his", "her", "its", "our", "their", "each", "every", "some", "any",
    "no", "all", "both", "few", "many", "much", "several",
    # Pronouns
    "i", "me", "you", "he", "him", "she", "her", "it", "we", "us",
    "they", "them", "who", "whom", "which", "what", "myself", "yourself",
    "himself", "herself", "itself", "ourselves", "themselves",
    # Auxiliaries
    "is", "am", "are", "was", "were", "be", "been", "being",
    "do", "does", "did", "have", "has", "had", "having",
    "will", "would", "shall", "should", "can", "could", "may", "might",
    "must", "need", "dare", "ought",
    # Discourse markers
    "actually", "basically", "literally", "honestly", "really", "just",
    "like", "well", "okay", "right", "now", "then", "here", "there",
    # Negations
    "not", "never", "no",
}

# spaCy POS tags for function words
FUNCTION_POS_TAGS: set[str] = {
    "ADP",    # preposition
    "AUX",    # auxiliary
    "CCONJ",  # coordinating conjunction
    "DET",    # determiner
    "PART",   # particle
    "PRON",   # pronoun
    "SCONJ",  # subordinating conjunction
    "PUNCT",  # punctuation
    "INTJ",   # interjection (discourse markers)
    "ADV",    # adverbs (many are function-like: actually, basically, etc.)
}


class SentenceSkeletonExtractor:
    """Extracts function-word skeletons and computes the 6-cluster stylometry profile.

    Spec §Step 4: 'Strip all content nouns and verbs from each Thought_Unit.
    Retain only: function words, conjunctions, prepositions, determiners,
    pronouns, punctuation, and discourse markers.'

    These 6 cluster groups form the core of the Positive Space Object (60-variable profile).
    """

    def __init__(self, spacy_model=None):
        """Initialize with optional spaCy model.

        Args:
            spacy_model: Pre-loaded spaCy model (en_core_web_sm).
                If None, falls back to regex-based function word extraction.
        """
        self.nlp = spacy_model

    def extract(
        self,
        corpus: ExtractionCorpus,
        invariant_markers: Optional[list[str]] = None,
    ) -> StylometryProfile:
        """Execute Step 4: Sentence Skeleton Extraction.

        Args:
            corpus: Assembled extraction corpus from Step 1.
            invariant_markers: Markers that passed cross-topic invariance (Step 3).

        Returns:
            StylometryProfile with all 6 cluster groups populated.
        """
        full_text = " ".join(u.text for u in corpus.units)
        sentences = self._split_sentences(full_text)

        # Extract function word skeletons
        skeletons = self._extract_skeletons(corpus)

        # Build all 6 clusters
        profile = StylometryProfile(
            lexical=self._compute_lexical_cluster(full_text),
            syntactic=self._compute_syntactic_cluster(full_text, skeletons),
            wan_metrics=self._compute_wan_metrics(skeletons),
            graphical=self._compute_graphical_cluster(full_text, sentences),
            structural=self._compute_structural_cluster(sentences, corpus),
            invariant_markers=invariant_markers or [],
        )

        profile.compute_hash()
        return profile

    # ──────────────────────────────────────────────────────────
    # Skeleton Extraction
    # ──────────────────────────────────────────────────────────

    def _extract_skeletons(self, corpus: ExtractionCorpus) -> list[list[str]]:
        """Extract function-word skeletons from all corpus units.

        Returns a list of function-word token lists (one per unit).
        """
        skeletons: list[list[str]] = []

        for unit in corpus.units:
            if self.nlp is not None:
                skeleton = self._spacy_skeleton(unit.text)
            else:
                skeleton = self._regex_skeleton(unit.text)
            skeletons.append(skeleton)

        return skeletons

    def _spacy_skeleton(self, text: str) -> list[str]:
        """Extract skeleton using spaCy POS tags."""
        nlp = self.nlp
        if nlp is None:
            return self._regex_skeleton(text)
        doc = nlp(text)
        return [
            token.lower_ for token in doc
            if token.pos_ in FUNCTION_POS_TAGS or token.lower_ in FUNCTION_WORDS
        ]

    def _regex_skeleton(self, text: str) -> list[str]:
        """Fallback: extract skeleton using the FUNCTION_WORDS set."""
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if w in FUNCTION_WORDS]

    # ──────────────────────────────────────────────────────────
    # Cluster 1: Lexical/Morphological
    # ──────────────────────────────────────────────────────────

    def _compute_lexical_cluster(self, text: str) -> LexicalMorphologicalCluster:
        """Spec §Step 4 Cluster 1: TTR, hapax legomena frequency, vocabulary density."""
        words = re.findall(r"\b[a-z]+\b", text.lower())
        if not words:
            return LexicalMorphologicalCluster()

        total = len(words)
        unique = set(words)
        unique_count = len(unique)
        counter = Counter(words)

        # Hapax legomena = words that appear exactly once
        hapax_count = sum(1 for w, c in counter.items() if c == 1)

        return LexicalMorphologicalCluster(
            type_token_ratio=unique_count / total if total else 0.0,
            hapax_legomena_frequency=hapax_count / total if total else 0.0,
            vocabulary_density=unique_count / (total ** 0.5) if total else 0.0,
            unique_word_count=unique_count,
            total_word_count=total,
        )

    # ──────────────────────────────────────────────────────────
    # Cluster 2: Subconscious Syntactic Distributions
    # ──────────────────────────────────────────────────────────

    def _compute_syntactic_cluster(
        self, text: str, skeletons: list[list[str]]
    ) -> SyntacticDistributionCluster:
        """Spec §Step 4 Cluster 2: Function word ratios, clause connective patterns."""
        all_function_words = [w for skel in skeletons for w in skel]
        total_fw = len(all_function_words) or 1
        counter = Counter(all_function_words)

        return SyntacticDistributionCluster(
            and_density=counter.get("and", 0) / total_fw,
            but_density=counter.get("but", 0) / total_fw,
            so_density=counter.get("so", 0) / total_fw,
            because_density=counter.get("because", 0) / total_fw,
            if_density=counter.get("if", 0) / total_fw,
            clause_connective_ratio=sum(
                counter.get(w, 0) for w in [
                    "because", "although", "though", "while", "since",
                    "unless", "until", "if", "when", "where", "whereas",
                ]
            ) / total_fw,
        )

    # ──────────────────────────────────────────────────────────
    # Cluster 3: Relational WAN Metrics
    # ──────────────────────────────────────────────────────────

    def _compute_wan_metrics(
        self, skeletons: list[list[str]]
    ) -> WANMetricsCluster:
        """Spec §Step 4 Cluster 3: Preposition-conjunction transition probabilities.

        WAN = Word Adjacency Network. We compute transition probabilities
        between consecutive function words in skeletons.
        """
        PREPS = {
            "in", "on", "at", "to", "from", "by", "with", "without", "about",
            "through", "during", "before", "after", "between", "among", "into",
            "out", "over", "under", "above", "below", "around", "against",
        }
        CONJS = {
            "and", "but", "or", "nor", "so", "because", "although", "though",
            "while", "since", "unless", "until", "if", "when", "where",
        }

        transition_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        pair_counts: list[tuple[str, str, int]] = []

        for skeleton in skeletons:
            for i in range(len(skeleton) - 1):
                w1, w2 = skeleton[i], skeleton[i + 1]
                if w1 in PREPS | CONJS and w2 in PREPS | CONJS:
                    transition_counts[w1][w2] += 1

        # Normalize to probabilities
        transition_probs: dict[str, dict[str, float]] = {}
        for w1, targets in transition_counts.items():
            total = sum(targets.values())
            if total > 0:
                transition_probs[w1] = {
                    w2: count / total for w2, count in targets.items()
                }

        # Top adjacency pairs
        all_pairs: list[tuple[str, str, int]] = []
        for w1, targets in transition_counts.items():
            for w2, count in targets.items():
                all_pairs.append((w1, w2, count))
        all_pairs.sort(key=lambda x: x[2], reverse=True)
        top_pairs = [(a, b, float(c)) for a, b, c in all_pairs[:20]]

        # Network density = actual edges / possible edges
        unique_nodes = set()
        for w1, targets in transition_counts.items():
            unique_nodes.add(w1)
            unique_nodes.update(targets.keys())
        n = len(unique_nodes)
        possible = n * (n - 1) if n > 1 else 1
        actual = sum(len(t) for t in transition_counts.values())

        return WANMetricsCluster(
            transition_probabilities=transition_probs,
            adjacency_pairs=top_pairs,
            network_density=actual / possible if possible else 0.0,
        )

    # ──────────────────────────────────────────────────────────
    # Cluster 4: Graphical Habits
    # ──────────────────────────────────────────────────────────

    def _compute_graphical_cluster(
        self, text: str, sentences: list[str]
    ) -> GraphicalHabitsCluster:
        """Spec §Step 4 Cluster 4: Punctuation density, capitalization anomalies."""
        words = text.split()
        total_words = len(words) or 1
        total_sentences = len(sentences) or 1

        # Em-dash per 100 words
        em_dash_count = text.count("—") + text.count(" - ")
        em_dash_per_100 = (em_dash_count / total_words) * 100

        # Ellipsis frequency
        ellipsis_count = text.count("...") + text.count("…")
        ellipsis_freq = ellipsis_count / total_words

        # Comma load per sentence
        comma_count = text.count(",")
        comma_per_sentence = comma_count / total_sentences

        # Exclamation frequency
        exclamation_count = text.count("!")
        exclamation_freq = exclamation_count / total_sentences

        # Capitalization anomalies: mid-sentence capitals not starting a sentence
        cap_anomaly_count = 0
        for sent in sentences:
            words_in_sent = sent.split()
            for word in words_in_sent[1:]:  # Skip first word
                if word and word[0].isupper() and not word.isupper() and word not in {"I"}:
                    # Check it's not a common proper noun pattern
                    if len(word) > 1 and word[1:].islower():
                        cap_anomaly_count += 1
        cap_anomaly_rate = cap_anomaly_count / total_words

        return GraphicalHabitsCluster(
            em_dash_per_100_words=em_dash_per_100,
            ellipsis_frequency=ellipsis_freq,
            comma_load_per_sentence=comma_per_sentence,
            exclamation_frequency=exclamation_freq,
            capitalization_anomaly_rate=cap_anomaly_rate,
        )

    # ──────────────────────────────────────────────────────────
    # Cluster 5: Structural Complexity
    # ──────────────────────────────────────────────────────────

    def _compute_structural_cluster(
        self, sentences: list[str], corpus: ExtractionCorpus
    ) -> StructuralComplexityCluster:
        """Spec §Step 4 Cluster 5: WPS flow, paragraph-to-paragraph length variance."""
        if not sentences:
            return StructuralComplexityCluster()

        wps_values = [len(s.split()) for s in sentences]

        mean = statistics.mean(wps_values)
        median = statistics.median(wps_values)
        std_dev = statistics.stdev(wps_values) if len(wps_values) > 1 else 0.0
        short_ratio = sum(1 for w in wps_values if w <= 5) / len(wps_values)
        long_ratio = sum(1 for w in wps_values if w >= 20) / len(wps_values)

        # Paragraph-level variance (use units as paragraphs)
        unit_lengths = [u.word_count for u in corpus.units if u.word_count > 0]
        para_variance = statistics.variance(unit_lengths) if len(unit_lengths) > 1 else 0.0

        return StructuralComplexityCluster(
            wps_mean=mean,
            wps_median=median,
            wps_std_dev=std_dev,
            wps_flow_pattern=wps_values[:50],  # First 50 for pattern analysis
            paragraph_length_variance=para_variance,
            short_sentence_ratio=short_ratio,
            long_sentence_ratio=long_ratio,
        )

    # ──────────────────────────────────────────────────────────
    # Utilities
    # ──────────────────────────────────────────────────────────

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences using spaCy or regex fallback."""
        nlp = self.nlp
        if nlp is not None:
            doc = nlp(text)
            return [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        # Regex fallback
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]
