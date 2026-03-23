"""
CCP FR4 Emotional DNA — Granularity Triage (Unit 2)
Phase 2: Determines extraction depth via emotional term inventory.

Spec reference: FR4 Tech Spec §Phase 2 — REASON — Granularity Triage
Research basis: Barrett (2017) Emotional Granularity and Affect Labeling

Triage tiers:
  HIGH   (≥25 distinct terms): Full extraction viable (V1-V10 + all CSIP v3)
  MEDIUM (12-24 terms):       Standard extraction (V1-V10; CSIP v3 may be partial)
  LOW    (<12 terms):         Surface extraction (V1, V3, V5, V6-V10 only;
                               V2, V4 may not be extractable)
"""

import re
from typing import Optional

from src.ccp.models.emotional_dna_models import (
    GRANULARITY_HIGH_THRESHOLD,
    GRANULARITY_MEDIUM_THRESHOLD,
    GranularityTriageResult,
    TriageTier,
)


# ──────────────────────────────────────────────────────────────
# Emotional Term Lexicon
# ──────────────────────────────────────────────────────────────
# Words describing INTERNAL states — not external situations.
# Sourced from Barrett (2017) constructionist emotion categories,
# Scherer (2001) appraisal labels, and LIWC-22 affect categories.

EMOTIONAL_TERMS: set[str] = {
    # Primary emotions
    "anger", "angry", "rage", "furious", "fury", "outrage", "outraged",
    "irritated", "irritation", "annoyed", "frustrated", "frustration",
    "resentment", "resentful", "bitter", "bitterness",
    # Sadness / grief
    "sad", "sadness", "grief", "grieving", "sorrow", "sorrowful",
    "heartbroken", "heartbreak", "despair", "despairing", "mourning",
    "loss", "lonely", "loneliness", "melancholy",
    # Fear / anxiety
    "fear", "afraid", "scared", "terrified", "terror", "anxious",
    "anxiety", "worried", "worry", "dread", "dreading", "panic",
    "panicked", "nervous", "apprehensive", "uneasy",
    # Joy / positive
    "happy", "happiness", "joy", "joyful", "elated", "elation",
    "excited", "excitement", "thrilled", "ecstatic", "euphoric",
    "delighted", "delight", "grateful", "gratitude", "bliss",
    "passionate", "passion", "fulfilled", "fulfillment",
    # Disgust
    "disgust", "disgusted", "revolted", "repulsed", "contempt",
    "contemptuous", "loathing", "repulsion",
    # Surprise
    "surprised", "surprise", "shocked", "shock", "astonished",
    "amazed", "stunned", "bewildered",
    # Shame / guilt
    "shame", "ashamed", "guilty", "guilt", "embarrassed",
    "embarrassment", "humiliated", "humiliation", "regret",
    # Tenderness / compassion
    "tender", "tenderness", "compassion", "compassionate",
    "empathy", "empathetic", "warmth", "caring", "gentle",
    "nurturing", "loving", "love",
    # Conviction / urgency
    "conviction", "convinced", "determined", "determination",
    "urgent", "urgency", "driven", "compelled", "resolute",
    # Complex emotional states
    "vulnerable", "vulnerability", "overwhelmed", "exhausted",
    "burned out", "burnout", "hopeful", "hope", "hopeless",
    "helpless", "powerless", "empowered", "liberated",
    "trapped", "suffocated", "relieved", "relief",
    "conflicted", "torn", "ambivalent", "nostalgic",
    "jealous", "jealousy", "envious", "envy",
    "proud", "pride", "awe", "inspired", "inspiration",
}


class GranularityTriageService:
    """Executes Phase 2 granularity triage on the extraction corpus.

    Spec §Phase 2: 'Scan full corpus for distinct emotional terms —
    words describing internal states, not external situations.'

    The triage tier determines which variables can be extracted.
    This gate is non-negotiable — extraction below triage depth
    produces fabricated variables.
    """

    def __init__(self, additional_terms: Optional[set[str]] = None):
        """Initialize with optional additional emotional terms.

        Args:
            additional_terms: Domain-specific emotional terms to add
                to the base lexicon.
        """
        self.emotional_terms = EMOTIONAL_TERMS.copy()
        if additional_terms:
            self.emotional_terms.update(additional_terms)

    def triage(self, corpus_text: str) -> GranularityTriageResult:
        """Execute granularity triage on the full corpus text.

        Args:
            corpus_text: Full concatenated corpus text from all transcripts.

        Returns:
            GranularityTriageResult with tier classification and term inventory.
        """
        # Extract all words, lowercased
        words = re.findall(r"\b[a-z][a-z\s'-]+\b", corpus_text.lower())
        word_set = set(words)

        # Find distinct emotional terms present in corpus
        found_terms = sorted(word_set & self.emotional_terms)
        distinct_count = len(found_terms)

        # Classify tier
        if distinct_count >= GRANULARITY_HIGH_THRESHOLD:
            tier = TriageTier.HIGH
            depth_note = (
                f"Full extraction viable — {distinct_count} distinct emotional terms "
                f"detected (threshold: {GRANULARITY_HIGH_THRESHOLD}). "
                "V1-V10 + all CSIP v3 extensions extractable."
            )
        elif distinct_count >= GRANULARITY_MEDIUM_THRESHOLD:
            tier = TriageTier.MEDIUM
            depth_note = (
                f"Standard extraction — {distinct_count} distinct emotional terms "
                f"detected (range: {GRANULARITY_MEDIUM_THRESHOLD}-"
                f"{GRANULARITY_HIGH_THRESHOLD - 1}). "
                "V1-V10 extractable; CSIP v3 may be partial."
            )
        else:
            tier = TriageTier.LOW
            depth_note = (
                f"Surface extraction only — {distinct_count} distinct emotional terms "
                f"detected (below {GRANULARITY_MEDIUM_THRESHOLD}). "
                "V1, V3, V5, V6-V10 extractable. "
                "V2 (Appraisal Sequence) and V4 (Norm Compatibility) "
                "may not be extractable — flag for enhanced interview."
            )

        return GranularityTriageResult(
            tier=tier,
            distinct_emotional_term_count=distinct_count,
            emotional_terms_found=found_terms,
            extraction_depth_note=depth_note,
        )

    def can_extract_variable(
        self, variable_name: str, tier: TriageTier
    ) -> bool:
        """Determine if a variable can be extracted at the given triage tier.

        Spec §Phase 2: LOW tier → V2 and V4 may not be extractable.

        Args:
            variable_name: Variable identifier (e.g., "V2", "V4", "EXT-1").
            tier: The triage tier classification.

        Returns:
            True if extraction is permitted at this tier.
        """
        if tier == TriageTier.HIGH:
            return True

        if tier == TriageTier.MEDIUM:
            # All V1-V10 extractable; CSIP may be partial but attempt permitted
            return True

        # LOW tier: V2 and V4 are NOT extractable
        if tier == TriageTier.LOW:
            blocked_at_low = {"V2", "V4"}
            return variable_name not in blocked_at_low

        return False
