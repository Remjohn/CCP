"""
Cultural Frame Detector — Architecture Layer 2E

Classifies the cultural expression style of journal entries and
detects code-switching patterns. Essential for preventing systematic
scoring errors with collectivist and diasporic users.

Two core functions:
    1. detect_cultural_frame()  — classifies expression style
    2. detect_code_switches()   — identifies language boundary switches

Without this detector, collectivist users receive systematically wrong
identity scores because their indirect identity expression triggers
false negatives in the Narrative Identity Scorer.

Academic basis: Cross-Cultural Identity Expression in Voice (Paper 3),
Markus & Kitayama (1991) independent vs. interdependent self-construal.
"""

import re
import logging
from dataclasses import dataclass, field
from typing import Optional

from backend.core.identity_models import CulturalFrame, ConfidenceLevel

logger = logging.getLogger(__name__)

# ─── Code Switch Detection ──────────────────────────────────────────

# Common French patterns (for French-English code-switching detection)
_FRENCH_MARKERS = [
    "je ", "tu ", "il ", "elle ", "nous ", "vous ", "ils ", "elles ",
    "c'est", "j'ai", "je suis", "il faut", "on est", "tu sais",
    "mais", "parce que", "quand même", "n'est-ce pas", "voilà",
    "ça va", "d'accord", "en fait", "tout à fait", "bien sûr",
    "pas facile", "très bien", "mon frère", "ma soeur", "la famille",
    "wallah", "inshallah",  # Arabic markers common in French-African diaspora
]

# Common Arabic markers (for French-Arabic code-switching)
_ARABIC_MARKERS = [
    "hamdulillah", "inshallah", "mashallah", "wallah", "yalla",
    "habibi", "habibti", "akhi", "oumma", "deen",
]


@dataclass
class CodeSwitch:
    """A detected language boundary switch within text."""
    position: int              # Character index in text
    from_lang: str             # Language before switch
    to_lang: str               # Language after switch
    switch_text: str           # The phrase that triggered detection
    social_function: str       # IDENTITY_MARKING or COMMUNICATIVE_STRATEGY


def detect_code_switches(text: str) -> list[CodeSwitch]:
    """
    Identifies language boundary switches within the journal text.

    Cognitive state: Language boundary pattern detection.
    You are scanning for the moments where the writer shifts from one
    language to another within the same entry. The critical distinction
    is the social function of each switch:
      - IDENTITY_MARKING: asserting heritage, culture, or in-group membership
        (e.g., switching to Arabic for family concepts, to French for emotional
        expressions). These switches ARE identity signals.
      - COMMUNICATIVE_STRATEGY: seeking clarity or precision
        (e.g., switching to English for technical terms). These switches
        are NOT identity signals.
    """
    switches = []
    text_lower = text.lower()

    # Check for French markers within predominantly English text
    english_word_ratio = _estimate_english_ratio(text)

    for marker in _FRENCH_MARKERS:
        marker_lower = marker.lower()
        idx = text_lower.find(marker_lower)
        while idx != -1:
            # Determine if this is identity-marking or communicative
            context = text_lower[max(0, idx - 30):idx + len(marker) + 30]
            social_fn = _classify_switch_function(marker_lower, context)

            switches.append(CodeSwitch(
                position=idx,
                from_lang="en",
                to_lang="fr",
                switch_text=marker.strip(),
                social_function=social_fn,
            ))
            idx = text_lower.find(marker_lower, idx + len(marker))

    for marker in _ARABIC_MARKERS:
        marker_lower = marker.lower()
        idx = text_lower.find(marker_lower)
        while idx != -1:
            # Arabic/religious markers in English/French context are almost always identity-marking
            switches.append(CodeSwitch(
                position=idx,
                from_lang="en",
                to_lang="ar",
                switch_text=marker.strip(),
                social_function="IDENTITY_MARKING",
            ))
            idx = text_lower.find(marker_lower, idx + len(marker))

    # Deduplicate by position (keep unique switches only)
    seen_positions = set()
    unique_switches = []
    for sw in sorted(switches, key=lambda s: s.position):
        if sw.position not in seen_positions:
            seen_positions.add(sw.position)
            unique_switches.append(sw)

    return unique_switches


def _classify_switch_function(marker: str, context: str) -> str:
    """
    Classifies whether a code-switch is IDENTITY_MARKING or COMMUNICATIVE_STRATEGY.

    Identity-marking switches involve:
    - Family/relational terms (ma famille, mon frère, la famille)
    - Emotional expressions (c'est pas facile, ça fait mal)
    - Religious/cultural terms (inshallah, hamdulillah, wallah)
    - In-group address forms (tu sais, mon frère)

    Communicative switches involve:
    - Technical terms without emotional weight
    - Clarification phrases (en fait, c'est-à-dire)
    """
    identity_contexts = [
        "famille", "frère", "soeur", "maman", "papa", "dieu",
        "coeur", "âme", "pas facile", "fait mal", "tu sais",
        "mon frère", "ma soeur", "wallah", "hamdulillah",
    ]

    for ic in identity_contexts:
        if ic in context.lower():
            return "IDENTITY_MARKING"

    return "COMMUNICATIVE_STRATEGY"


def _estimate_english_ratio(text: str) -> float:
    """Rough estimate of English word ratio in text."""
    words = text.lower().split()
    if not words:
        return 1.0

    # Common English stop words as proxy
    english_stops = {"the", "is", "at", "in", "on", "to", "a", "and", "of", "for", "it", "my", "i"}
    english_count = sum(1 for w in words if w in english_stops)
    return english_count / len(words)


# ─── Cultural Frame Detection ───────────────────────────────────────

def detect_cultural_frame(text: str) -> tuple[CulturalFrame, ConfidenceLevel]:
    """
    Classifies the journal entry's cultural expression style using 3 signal layers.

    Cognitive state: Cultural pattern recognition.
    You are identifying HOW this person constructs self-narrative,
    not WHAT they say. Two people describing the same achievement
    use different structures based on cultural self-construal:
      - Direct/Individualist: "I achieved this because I worked hard"
      - Relational/Collectivist: "We got through this as a family"
      - Hybrid/Diasporic: Both patterns + language switches

    Signal Layer 1: Pronoun ratio (I/me vs. we/our)
    Signal Layer 2: Syntactic structure (agentive vs. relational)
    Signal Layer 3: Code-switching presence
    """
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)

    if word_count < 20:
        return CulturalFrame.DIRECT_INDIVIDUALIST, ConfidenceLevel.LOW

    # ── Signal Layer 1: Pronoun Ratio ──
    i_pronouns = sum(1 for w in words if w in ("i", "me", "my", "mine", "myself",
                                                  "je", "moi", "mon", "ma", "mes"))
    we_pronouns = sum(1 for w in words if w in ("we", "us", "our", "ours", "ourselves",
                                                  "nous", "notre", "nos", "on"))

    total_pronouns = i_pronouns + we_pronouns
    if total_pronouns > 0:
        i_ratio = i_pronouns / total_pronouns
    else:
        i_ratio = 0.5  # Neutral if no pronouns

    # ── Signal Layer 2: Agentive vs. Relational structure ──
    # Agentive: "I decided/chose/built/created/conquered"
    agentive_verbs = ["decided", "chose", "built", "created", "conquered",
                      "achieved", "won", "dominated", "controlled", "grabbed"]
    relational_verbs = ["shared", "supported", "connected", "belonged",
                        "honored", "served", "maintained", "provided", "endured"]

    agentive_count = sum(1 for v in agentive_verbs if v in text_lower)
    relational_count = sum(1 for v in relational_verbs if v in text_lower)

    # ── Signal Layer 3: Code-switching ──
    code_switches = detect_code_switches(text)
    identity_switches = [cs for cs in code_switches if cs.social_function == "IDENTITY_MARKING"]

    # ── Classification Logic ──
    # Hybrid/Diasporic: ≥2 code switches within the entry
    if len(code_switches) >= 2:
        return CulturalFrame.HYBRID_DIASPORIC, ConfidenceLevel.HIGH

    # Relational/Collectivist: high we-pronoun ratio + relational verbs
    if i_ratio < 0.4 and relational_count > agentive_count:
        confidence = ConfidenceLevel.HIGH if (i_ratio < 0.3 and relational_count >= 2) else ConfidenceLevel.MEDIUM
        return CulturalFrame.RELATIONAL_COLLECTIVIST, confidence

    # Direct/Individualist: high I-pronoun ratio + agentive verbs
    if i_ratio > 0.6 and agentive_count >= relational_count:
        confidence = ConfidenceLevel.HIGH if (i_ratio > 0.7 and agentive_count >= 2) else ConfidenceLevel.MEDIUM
        return CulturalFrame.DIRECT_INDIVIDUALIST, confidence

    # Default with low confidence if signals are mixed
    if i_ratio > 0.5:
        return CulturalFrame.DIRECT_INDIVIDUALIST, ConfidenceLevel.LOW
    elif i_ratio < 0.5:
        return CulturalFrame.RELATIONAL_COLLECTIVIST, ConfidenceLevel.LOW
    else:
        return CulturalFrame.DIRECT_INDIVIDUALIST, ConfidenceLevel.LOW
