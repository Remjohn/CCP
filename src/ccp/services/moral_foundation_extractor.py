"""
CCP FR4 Emotional DNA — V6-V10 Moral Foundation Extractor (Unit 4)
Phase 3: Extract MFQ-2 moral foundation weight variables from corpus.

Spec reference: FR4 Tech Spec §Phase 3 Variables V6-V10
Research basis: MFQ-2 (Haidt & Joseph, 2004; Atari et al., 2022),
    Moral Foundations Dictionary 2.0

V6:  Care/Harm (weight)
V7:  Fairness/Cheating (weight + equality/proportionality sub-type)
V8:  Loyalty/Betrayal (weight)
V9:  Authority/Subversion (weight)
V10: Sanctity/Degradation (weight)
V10b: Liberty/Oppression (weight)

Constraint: Sum of V6-V10b weights = 1.0
Mandate 7 enforced: every foundation requires corpus citation.
"""

import re
from typing import Optional

from src.ccp.models.emotional_dna_models import (
    MFT_MINIMUM_EVIDENCE_PASSAGES,
    ClusterAlignment,
    EvidencePassage,
    FairnessSubType,
    MoralFoundations,
    MoralFoundationWeight,
    V7FairnessCheating,
    V10SanctityDegradation,
    V10bLibertyOppression,
)


# ──────────────────────────────────────────────────────────────
# MFD 2.0 Keyword Dictionaries
# Spec §Phase 3: "Apply MFD 2.0 keyword lists"
# ──────────────────────────────────────────────────────────────

MFD_CARE_HARM: set[str] = {
    "compassion", "compassionate", "empathy", "empathetic", "sympathy",
    "suffering", "harm", "hurt", "pain", "cruel", "cruelty", "kindness",
    "care", "caring", "nurture", "nurturing", "gentle", "protect",
    "vulnerable", "vulnerable", "safe", "safety", "abuse", "abused",
    "trauma", "traumatic", "wound", "wounded", "heal", "healing",
    "tender", "sensitive", "mercy", "pity", "rescue", "comfort",
    "neglect", "neglected", "benevolence", "warmth",
}

MFD_FAIRNESS_CHEATING: set[str] = {
    "fair", "fairness", "unfair", "justice", "injustice", "unjust",
    "equal", "equality", "equitable", "inequity", "rights", "deserve",
    "deserved", "entitle", "entitled", "cheat", "cheated", "cheating",
    "fraud", "reciprocity", "reciprocal", "bias", "biased", "balanced",
    "impartial", "partial", "merit", "meritocracy", "proportional",
    "proportionality", "discrimination", "discriminate",
}

# V7 sub-type keyword sets
MFD_FAIRNESS_EQUALITY: set[str] = {
    "equal", "equality", "equitable", "same", "everyone",
    "universal", "egalitarian", "redistribution", "level playing field",
    "no one should", "across the board", "regardless",
}
MFD_FAIRNESS_PROPORTIONALITY: set[str] = {
    "proportional", "proportionality", "earned", "deserve",
    "merit", "meritocracy", "worked for", "you get what",
    "effort", "contribution", "reward", "performance",
}

MFD_LOYALTY_BETRAYAL: set[str] = {
    "loyalty", "loyal", "disloyal", "betrayal", "betray", "betrayed",
    "tribe", "tribal", "team", "solidarity", "unity", "patriot",
    "patriotic", "treason", "traitor", "turncoat", "belong",
    "belonging", "us", "them", "in-group", "out-group", "fidelity",
    "faithfulness", "devotion", "commitment", "allegiance",
}

MFD_AUTHORITY_SUBVERSION: set[str] = {
    "authority", "authoritative", "respect", "obey", "obedience",
    "hierarchy", "order", "tradition", "traditional", "discipline",
    "duty", "submit", "submission", "rebel", "rebellion", "subvert",
    "subversion", "deference", "rank", "leader", "leadership",
    "legitimate", "illegitimate", "role", "status", "elder",
}

MFD_SANCTITY_DEGRADATION: set[str] = {
    "sanctity", "sacred", "holy", "divine", "pure", "purity",
    "impure", "pollute", "polluted", "contaminate", "degradation",
    "degrade", "degrading", "disgust", "disgusting", "filth",
    "filthy", "clean", "cleanse", "untouched", "pristine",
    "desecrate", "profane", "virtue", "virtuous", "noble",
    "elevation", "transcend", "transcendence", "wholesome",
}

MFD_LIBERTY_OPPRESSION: set[str] = {
    "liberty", "freedom", "free", "oppression", "oppressed",
    "oppressive", "tyranny", "tyrant", "autonomy", "independent",
    "independence", "sovereign", "sovereignty", "coercion", "coerce",
    "control", "controlling", "dominate", "domination", "consent",
    "voluntary", "choice", "self-determination", "emancipation",
    "liberation", "restriction", "restricted", "constraint",
}


# Foundation name → keyword set mapping
FOUNDATION_KEYWORDS: dict[str, set[str]] = {
    "care_harm": MFD_CARE_HARM,
    "fairness_cheating": MFD_FAIRNESS_CHEATING,
    "loyalty_betrayal": MFD_LOYALTY_BETRAYAL,
    "authority_subversion": MFD_AUTHORITY_SUBVERSION,
    "sanctity_degradation": MFD_SANCTITY_DEGRADATION,
    "liberty_oppression": MFD_LIBERTY_OPPRESSION,
}

# Cluster membership: Individualizing = Care + Fairness; Binding = Loyalty + Authority + Sanctity
INDIVIDUALIZING_FOUNDATIONS: set[str] = {"care_harm", "fairness_cheating"}
BINDING_FOUNDATIONS: set[str] = {"loyalty_betrayal", "authority_subversion", "sanctity_degradation"}


def _tokenize_lower(text: str) -> list[str]:
    """Tokenize text to lowercase words (preserving hyphens)."""
    return re.findall(r"[a-z]+(?:-[a-z]+)*", text.lower())


def _count_foundation_hits(
    tokens: list[str],
    keyword_set: set[str],
) -> int:
    """Count how many tokens are in the keyword set."""
    count = 0
    for token in tokens:
        if token in keyword_set:
            count += 1
    return count


def _find_evidence_sentences(
    sentences: list[str],
    keyword_set: set[str],
    label: str,
    session_id: str,
    max_passages: int = 10,
) -> list[EvidencePassage]:
    """Find sentences containing keywords from the set."""
    passages: list[EvidencePassage] = []
    for idx, sent in enumerate(sentences):
        sent_lower = sent.lower()
        hits = [kw for kw in keyword_set if kw in sent_lower]
        if hits:
            passages.append(EvidencePassage(
                passage_text=sent.strip(),
                passage_index=idx,
                label=f"{label}:{','.join(hits[:3])}",
                source_session_id=session_id,
            ))
            if len(passages) >= max_passages:
                break
    return passages


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


class MoralFoundationExtractor:
    """Extracts V6-V10 Moral Foundation weights from corpus.

    Spec §Phase 3: Apply MFD 2.0 keyword lists, calculate frequency-based
    weights, classify primary/secondary foundations, determine cluster
    alignment (Individualizing vs Binding).
    """

    def extract(
        self,
        corpus_text: str,
        session_id: str = "",
    ) -> MoralFoundations:
        """Extract all V6-V10b moral foundation weights.

        Args:
            corpus_text: Full concatenated corpus text.
            session_id: Source session ID for evidence provenance.

        Returns:
            MoralFoundations with weights summing to 1.0.
        """
        tokens = _tokenize_lower(corpus_text)
        sentences = _split_into_sentences(corpus_text)

        # Count keyword hits per foundation
        raw_counts: dict[str, int] = {}
        for name, keyword_set in FOUNDATION_KEYWORDS.items():
            raw_counts[name] = _count_foundation_hits(tokens, keyword_set)

        total_hits = sum(raw_counts.values())

        if total_hits == 0:
            return MoralFoundations()

        # Calculate normalized weights: weight = count / total
        weights: dict[str, float] = {
            name: round(count / total_hits, 4) if total_hits > 0 else 0.0
            for name, count in raw_counts.items()
        }

        # Collect evidence for each foundation
        evidence: dict[str, list[EvidencePassage]] = {}
        for name, keyword_set in FOUNDATION_KEYWORDS.items():
            evidence[name] = _find_evidence_sentences(
                sentences, keyword_set, name, session_id
            )

        # Build foundation objects
        result = MoralFoundations()

        # V6: Care/Harm
        result.v6_care_harm = MoralFoundationWeight(
            weight=weights["care_harm"],
            evidence_passages=evidence["care_harm"],
        )

        # V7: Fairness/Cheating + sub-type
        fairness_sub_type = self._classify_fairness_subtype(
            tokens, sentences, session_id
        )
        result.v7_fairness_cheating = V7FairnessCheating(
            weight=weights["fairness_cheating"],
            evidence_passages=evidence["fairness_cheating"],
            sub_type=fairness_sub_type,
        )

        # V8: Loyalty/Betrayal
        result.v8_loyalty_betrayal = MoralFoundationWeight(
            weight=weights["loyalty_betrayal"],
            evidence_passages=evidence["loyalty_betrayal"],
        )

        # V9: Authority/Subversion
        result.v9_authority_subversion = MoralFoundationWeight(
            weight=weights["authority_subversion"],
            evidence_passages=evidence["authority_subversion"],
        )

        # V10: Sanctity/Degradation
        result.v10_sanctity_degradation = V10SanctityDegradation(
            weight=weights["sanctity_degradation"],
            evidence_passages=evidence["sanctity_degradation"],
        )

        # V10b: Liberty/Oppression
        result.v10b_liberty_oppression = V10bLibertyOppression(
            weight=weights["liberty_oppression"],
            evidence_passages=evidence["liberty_oppression"],
        )

        # Primary and secondary foundations
        sorted_weights = sorted(
            weights.items(), key=lambda x: x[1], reverse=True
        )
        if sorted_weights:
            result.primary_foundation = sorted_weights[0][0]
            if (
                len(sorted_weights) > 1
                and sorted_weights[1][1] > 0
            ):
                # Spec: record secondary if substantial (≥ 15% of total)
                if sorted_weights[1][1] >= 0.15:
                    result.secondary_foundation = sorted_weights[1][0]

        # Cluster alignment
        result.cluster_alignment = self._determine_cluster_alignment(weights)

        return result

    def _classify_fairness_subtype(
        self,
        tokens: list[str],
        sentences: list[str],
        session_id: str,
    ) -> Optional[FairnessSubType]:
        """Spec §Phase 3 V7: Determine equality vs proportionality sub-type.

        Classify based on which sub-type keyword set has more hits.
        """
        equality_count = _count_foundation_hits(tokens, MFD_FAIRNESS_EQUALITY)
        proportionality_count = _count_foundation_hits(
            tokens, MFD_FAIRNESS_PROPORTIONALITY
        )

        # Need minimum signal to classify
        combined = equality_count + proportionality_count
        if combined < MFT_MINIMUM_EVIDENCE_PASSAGES:
            return None

        if equality_count > proportionality_count:
            return FairnessSubType.EQUALITY
        elif proportionality_count > equality_count:
            return FairnessSubType.PROPORTIONALITY
        else:
            return None  # Ambiguous — no sub-type determination

    def _determine_cluster_alignment(
        self,
        weights: dict[str, float],
    ) -> ClusterAlignment:
        """Spec §Phase 3: Classify as Individualizing, Binding, or Balanced.

        Individualizing = Care + Fairness
        Binding = Loyalty + Authority + Sanctity
        Liberty/Oppression is not in either cluster per MFT standard.
        """
        individualizing_sum = sum(
            weights.get(f, 0.0) for f in INDIVIDUALIZING_FOUNDATIONS
        )
        binding_sum = sum(
            weights.get(f, 0.0) for f in BINDING_FOUNDATIONS
        )

        # Normalize to just the 5 standard foundations (exclude liberty)
        liberty_w = weights.get("liberty_oppression", 0.0)
        five_foundation_total = 1.0 - liberty_w
        if five_foundation_total <= 0:
            return ClusterAlignment.BALANCED

        ind_pct = individualizing_sum / five_foundation_total
        bind_pct = binding_sum / five_foundation_total

        # Spec: determine cluster dominance
        if ind_pct >= 0.6:
            return ClusterAlignment.INDIVIDUALIZING
        elif bind_pct >= 0.6:
            return ClusterAlignment.BINDING
        else:
            return ClusterAlignment.BALANCED
