"""
CCP FR3 Negative Space Excavation — Unit 6
Mathematical extrapolation of the opposite of the invariant markers.

Spec reference: FR3 Tech Spec §Step 5 — Negative Space Excavation (MANDATE 4 — First DEP)
Agent: Valeriane
Stress test Q1: Gate PC-03 — L3 Minimum Depth ≥15 contrastive strings

GATE: This step must complete and produce a validated DEP-ENG-004 before
subsequent steps can execute. This is hardcoded in the pipeline orchestrator
— not a prompt instruction. (Mandate 4)

Three components of DEP-ENG-004:
  A. Lexical Blacklist — Words never used by the coach (academic, spiritual, banned intensifiers)
  B. Syntactic Impossibilities — Structural patterns with zero occurrence
  C. Structural Exclusions — Macro-level content structures never present
"""

import re
from collections import Counter
from typing import Optional

from src.ccp.models.voice_dna_models import (
    L3_MINIMUM_DEPTH_THRESHOLD,
    ExtractionCorpus,
    LexicalBlacklist,
    NegativeSpaceObject,
    StylometryProfile,
    StructuralExclusions,
)


class L3InsufficientDepthError(Exception):
    """Gate PC-03: L3 Minimum Depth Threshold not met.
    Stress test Q1: 'mathematically less than 15 validated contrastive strings
    → L3_INSUFFICIENT_DEPTH halt + Guardian Agent micro-interview.'"""
    pass


# ──────────────────────────────────────────────────────────────
# Reference word sets for blacklist comparison
# Common coaching vocabulary that the coach's corpus is compared against
# ──────────────────────────────────────────────────────────────

COMMON_ACADEMIC_COACHING_WORDS: list[str] = [
    "leverage", "paradigm", "holistic", "synergy", "methodology",
    "framework", "optimization", "implementation", "facilitation",
    "stakeholder", "competency", "bandwidth", "scalable", "alignment",
    "systemic", "modality", "taxonomy", "juxtaposition", "ontological",
    "epistemological", "phenomenological", "heuristic", "praxis",
    "synthesis", "dialectical", "normative", "schema", "meta-cognitive",
    "reductionist", "empirical", "constructivist", "pedagogical",
    "andragogical", "existential", "hermeneutic", "deontological",
]

COMMON_SPIRITUAL_COACHING_WORDS: list[str] = [
    "journey", "manifest", "universe", "vibration", "abundance",
    "alignment", "awakening", "consciousness", "transcend", "enlighten",
    "divine", "sacred", "chakra", "meditation", "presence",
    "surrender", "grace", "essence", "soul", "spirit", "karma",
    "dharma", "mindfulness", "flow", "oneness", "gratitude",
    "affirmation", "visualization", "quantum", "frequency", "energy",
    "intention", "destiny", "cosmic", "higher self", "inner child",
]

COMMON_INTENSIFIERS: list[str] = [
    "absolutely", "incredibly", "amazing", "transformative", "phenomenal",
    "extraordinary", "magnificent", "remarkable", "breathtaking",
    "spectacular", "unbelievable", "groundbreaking", "revolutionary",
    "life-changing", "game-changing", "mind-blowing", "jaw-dropping",
    "earth-shattering", "empowering", "inspiring", "awe-inspiring",
    "stellar", "superb", "exceptional", "outstanding",
]

# ──────────────────────────────────────────────────────────────
# Syntactic patterns to test for zero-occurrence
# ──────────────────────────────────────────────────────────────

SYNTACTIC_PATTERNS_TO_TEST: list[tuple[str, str]] = [
    ("Opens thought with a rhetorical question",
     r"^[A-Z][^.!]*\?"),
    ("Uses passive voice for personal experience claims",
     r"\b(?:I|my)\b.*\b(?:was|were|been)\b.*\b(?:given|told|shown|made|helped)\b"),
    ("Ends with resolved, tidy summary",
     r"(?:In summary|To sum up|In conclusion|The key takeaway|To recap)[^.]*\.\s*$"),
    ("Opens with a motivational quote",
     r'^"[^"]+"\s*[-—]'),
    ("Uses numbered lists in spoken content",
     r"(?:^|\n)\s*\d+[.)]\s"),
    ("Uses thesis-first declaration",
     r"^(?:The truth is|The fact is|Here's what I know|Let me be clear)[^.]*\."),
    ("Starts with a statistic or data point",
     r"^(?:\d+%|\d+ out of \d+|According to|Research shows|Studies indicate)"),
    ("Uses meta-commentary about their own speech",
     r"\b(?:What I'm trying to say|Let me rephrase|What I mean is|In other words)\b"),
    ("Employs triple emphasis punctuation",
     r"[!?]{3,}"),
    ("Uses bullet point structures verbally",
     r"(?:^|\n)\s*[-•]\s"),
    ("Transitions with textbook connectors",
     r"\b(?:Furthermore|Moreover|Additionally|Consequently|Subsequently|Notwithstanding)\b"),
    ("Closes with explicit call-to-action",
     r"(?:Go to|Sign up|Click|Subscribe|Download|Register|Join)[^.]*\.\s*$"),
]

# ──────────────────────────────────────────────────────────────
# Structural patterns to test
# ──────────────────────────────────────────────────────────────

OPENING_PATTERNS_TO_TEST: list[tuple[str, str]] = [
    ("thesis-first declaration", r"^(?:The truth is|Here's what|The fact is|I believe that)"),
    ("motivational quote lead", r'^"[^"]+"\s*[-—]'),
    ("statistic-first hook", r"^\d+%|^According to|^Research shows"),
    ("question-first hook", r"^(?:Have you ever|What if|Did you know)"),
    ("definition lead", r"^[A-Z][a-z]+ (?:is defined as|means|refers to)"),
    ("anecdote disclaimer", r"^(?:Let me tell you a story|I remember when|There was this time)"),
]

CLOSING_PATTERNS_TO_TEST: list[tuple[str, str]] = [
    ("CTA-explicit close", r"(?:Go to|Sign up|Click|Visit|Download|Get your)[^.]*\.\s*$"),
    ("listicle summary bullet points", r"(?:In summary|To recap).*(?:\d+[.)]|\n\s*[-•])"),
    ("callback-to-opening close", r"(?:Remember when I said|As I mentioned|Coming back to)"),
    ("neat motivational closer", r"(?:You've got this|Believe in yourself|The sky's the limit)"),
    ("academic conclusion", r"(?:In conclusion|To conclude|This demonstrates that|We can therefore)"),
    ("hashtag/social close", r"#\w+\s*$"),
]


class NegativeSpaceExcavator:
    """Excavates the Negative Space (DEP-ENG-004) from corpus analysis.

    Spec §Step 5: 'Mathematical extrapolation of the opposite of the
    invariant markers from Step 3.'

    Mandate 4: This DEP must be produced before DEP-ENG-003 can be extracted.
    Gate PC-03: Total contrastive strings must be ≥15.
    """

    def __init__(self, enforce_depth_gate: bool = True):
        """Initialize excavator.

        Args:
            enforce_depth_gate: If True, raises L3InsufficientDepthError when
                Gate PC-03 fails. Set False only for testing.
        """
        self.enforce_depth_gate = enforce_depth_gate

    def excavate(
        self,
        corpus: ExtractionCorpus,
        stylometry_profile: Optional[StylometryProfile] = None,
        invariant_markers: Optional[list[str]] = None,
    ) -> NegativeSpaceObject:
        """Execute Step 5: Negative Space Excavation.

        Args:
            corpus: Assembled extraction corpus from Step 1.
            stylometry_profile: StylometryProfile from Step 4 (for syntactic analysis).
            invariant_markers: Markers that passed cross-topic invariance (Step 3).

        Returns:
            NegativeSpaceObject (DEP-ENG-004) with all 3 components.

        Raises:
            L3InsufficientDepthError: If Gate PC-03 fails (< 15 contrastive strings).
        """
        full_text = " ".join(u.text for u in corpus.units)
        corpus_words = set(re.findall(r"\b[a-z]+\b", full_text.lower()))

        # Component A: Lexical Blacklist
        lexical_blacklist = self._excavate_lexical_blacklist(corpus_words)

        # Component B: Syntactic Impossibilities
        syntactic_impossibilities = self._excavate_syntactic_impossibilities(full_text)

        # Component C: Structural Exclusions
        structural_exclusions = self._excavate_structural_exclusions(corpus)

        neg_space = NegativeSpaceObject(
            lexical_blacklist=lexical_blacklist,
            syntactic_impossibilities=syntactic_impossibilities,
            structural_exclusions=structural_exclusions,
        )

        neg_space.compute_hash()

        # Gate PC-03: L3 Minimum Depth Threshold
        if self.enforce_depth_gate and not neg_space.passes_depth_gate():
            total = neg_space.total_contrastive_strings()
            raise L3InsufficientDepthError(
                f"Gate PC-03 FAILED: DEP-ENG-004 has {total} contrastive strings "
                f"but requires ≥{L3_MINIMUM_DEPTH_THRESHOLD}. "
                f"L3_INSUFFICIENT_DEPTH — Guardian Agent micro-interview required. "
                f"More Sacred Audio needed to increase Negative Space depth."
            )

        return neg_space

    def _excavate_lexical_blacklist(
        self, corpus_words: set[str]
    ) -> LexicalBlacklist:
        """Component A: Words common in coaching but NEVER used by this coach.

        Spec §Step 5: 'Academic vocabulary (words present in 0% of corpus but
        common in coaching content generally), Spiritual vocabulary (words present
        in coaching discourse generally but absent from this coach's corpus),
        Superlatives and intensifiers the coach never uses.'
        """
        academic = [
            word for word in COMMON_ACADEMIC_COACHING_WORDS
            if word.lower() not in corpus_words
        ]

        spiritual = [
            word for word in COMMON_SPIRITUAL_COACHING_WORDS
            if word.lower().split()[0] not in corpus_words  # Handle multi-word
        ]

        banned_intensifiers = [
            word for word in COMMON_INTENSIFIERS
            if word.lower().replace("-", "") not in corpus_words
        ]

        return LexicalBlacklist(
            academic=academic,
            spiritual=spiritual,
            banned_intensifiers=banned_intensifiers,
        )

    def _excavate_syntactic_impossibilities(
        self, full_text: str
    ) -> list[str]:
        """Component B: Structural patterns with zero occurrence in corpus.

        Spec §Step 5: 'Derived from the sentence skeleton analysis: patterns
        with zero occurrence across all subject clusters.
        Format: "The coach NEVER {syntactic pattern}"'
        """
        impossibilities: list[str] = []

        for label, pattern_str in SYNTACTIC_PATTERNS_TO_TEST:
            pattern = re.compile(pattern_str, re.MULTILINE | re.IGNORECASE)
            if not pattern.search(full_text):
                impossibilities.append(label)

        return impossibilities

    def _excavate_structural_exclusions(
        self, corpus: ExtractionCorpus
    ) -> StructuralExclusions:
        """Component C: Macro-level content structures never present.

        Spec §Step 5: 'Content opening types the coach never uses,
        Closing patterns the coach never uses.'
        """
        # Build lists of unit openings and closings for analysis
        openings = []
        closings = []
        for unit in corpus.units:
            text = unit.text.strip()
            if not text:
                continue
            # First sentence as "opening"
            first_sentences = re.split(r"(?<=[.!?])\s+", text)
            if first_sentences:
                openings.append(first_sentences[0])
            # Last sentence as "closing"
            if len(first_sentences) > 1:
                closings.append(first_sentences[-1])
            else:
                closings.append(first_sentences[0])

        opening_text = " ".join(openings)
        closing_text = " ".join(closings)

        forbidden_openings: list[str] = []
        for label, pattern_str in OPENING_PATTERNS_TO_TEST:
            pattern = re.compile(pattern_str, re.MULTILINE | re.IGNORECASE)
            if not pattern.search(opening_text):
                forbidden_openings.append(label)

        forbidden_closings: list[str] = []
        for label, pattern_str in CLOSING_PATTERNS_TO_TEST:
            pattern = re.compile(pattern_str, re.MULTILINE | re.IGNORECASE)
            if not pattern.search(closing_text):
                forbidden_closings.append(label)

        return StructuralExclusions(
            forbidden_openings=forbidden_openings,
            forbidden_closings=forbidden_closings,
        )

    def add_flagged_structure(
        self, neg_space: NegativeSpaceObject, flagged_structure: str
    ) -> NegativeSpaceObject:
        """Add a flagged structure from adversarial validation (Step 10 rewind).

        Spec §Step 10: 'The flagged structure is added to DEP-ENG-004's
        syntactic_impossibilities list.'
        """
        if flagged_structure not in neg_space.syntactic_impossibilities:
            neg_space.syntactic_impossibilities.append(flagged_structure)
        neg_space.compute_hash()
        return neg_space
