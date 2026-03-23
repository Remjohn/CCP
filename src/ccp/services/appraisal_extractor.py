"""
CCP FR4 Emotional DNA — V1-V5 Cognitive Appraisal Extractor (Unit 3)
Phase 3: Extract cognitive appraisal variables from corpus.

Spec reference: FR4 Tech Spec §Phase 3 Variables V1-V5
Research basis: Lazarus (1991), Scherer CPM (2001), Marsella & Gratch EMA

V1: Trigger Specificity Threshold (1-10)
V2: Appraisal Sequence Ordering (categorical)
V3: Coping Potential Pattern (ratio 0.0-1.0)
V4: Norm Compatibility Threshold (1-10)
V5: Agency Attribution Bias (categorical + dominant)

Mandate 7 enforced: every variable requires corpus citation.
"""

import re
from typing import Optional

from src.ccp.models.emotional_dna_models import (
    V1_MINIMUM_EVIDENCE_PASSAGES,
    V2_MINIMUM_PASSAGE_WORDS,
    V2_MINIMUM_PASSAGES,
    V3_MINIMUM_ACTION_PASSAGES,
    V3_MINIMUM_REFLECTIVE_PASSAGES,
    V4_MINIMUM_ANALYTICAL_PASSAGES,
    V4_MINIMUM_OUTRAGE_PASSAGES,
    V5_MINIMUM_ATTRIBUTION_PASSAGES,
    V5_MINIMUM_CATEGORIES,
    AgencyAttributionType,
    AppraisalSequenceType,
    AppraisalVariables,
    EvidencePassage,
    TriageTier,
    V1TriggerSpecificityThreshold,
    V2AppraisalSequenceOrdering,
    V3CopingPotentialPattern,
    V4NormCompatibilityThreshold,
    V5AgencyAttributionBias,
)


# ──────────────────────────────────────────────────────────────
# Keyword Indicators
# ──────────────────────────────────────────────────────────────

# V1: Activation transition markers (calm→emotional)
ACTIVATION_MARKERS: list[str] = [
    r"\b(what really gets me|what kills me|I can't stand|this is what)\b",
    r"\b(drives me crazy|makes my blood boil|breaks my heart)\b",
    r"\b(infuriates me|disgusts me|terrifies me|frustrates me)\b",
    r"\b(the moment I|when I see|every time I hear)\b",
    r"\b(I just can't|I refuse to|it's unacceptable)\b",
]

# V2: Appraisal sequence first-move indicators
MECHANISM_FIRST_MARKERS: list[str] = [
    r"\b(here's (how|why)|the mechanism is|what happens is)\b",
    r"\b(the way it works|the process is|structurally)\b",
    r"\b(let me explain|the reason this happens|technically)\b",
]
MORAL_VERDICT_FIRST_MARKERS: list[str] = [
    r"\b(this is wrong|it's unacceptable|it's disgusting)\b",
    r"\b(that's criminal|it's a disgrace|it's evil|morally)\b",
    r"\b(how dare|should be ashamed|there's no excuse)\b",
]
NARRATIVE_FIRST_MARKERS: list[str] = [
    r"\b(let me tell you|I remember when|there was this)\b",
    r"\b(story of|back when I|picture this|imagine)\b",
    r"\b(one time|I had a client who|I once)\b",
]
COPING_FIRST_MARKERS: list[str] = [
    r"\b(here's what (you|we) (need|should|can) do)\b",
    r"\b(the solution is|step one|first thing|the fix)\b",
    r"\b(stop doing|start doing|action item|my advice)\b",
]

# V3: Action vs Reflective indicators
ACTION_INDICATORS: list[str] = [
    r"\b(do this|take action|implement|execute|apply)\b",
    r"\b(here's what to do|the solution|fix this|step)\b",
    r"\b(go and|must do|should do|need to do|stop waiting)\b",
    r"\b(take the first|make the move|commit to|sign up)\b",
]
REFLECTIVE_INDICATORS: list[str] = [
    r"\b(what I've (observed|noticed|learned)|what this reveals)\b",
    r"\b(consider this|think about|reflect on|ponder)\b",
    r"\b(the deeper issue|underneath this|at the root)\b",
    r"\b(I wonder|it's interesting|the pattern is|notice how)\b",
]

# V4: Moral/outrage language
MORAL_LANGUAGE_MARKERS: list[str] = [
    r"\b(should|must|ought|wrong|right|evil|virtue|vice)\b",
    r"\b(disgrace|criminal|immoral|unethical|unjust|corrupt)\b",
    r"\b(betrayal|betrayed|violated|exploitation|exploitation)\b",
    r"\b(sacred|profane|dignity|honor|shame|dishonor)\b",
]

# V5: Agency attribution indicators
SELF_AGENCY_MARKERS: list[str] = [
    r"\b(you chose|your responsibility|take ownership|it's on you)\b",
    r"\b(personal accountability|you (decided|allowed)|own it)\b",
]
INDIVIDUAL_AGENCY_MARKERS: list[str] = [
    r"\b(these (people|leaders|practitioners)|specific (person|individual))\b",
    r"\b(he (did|failed|chose)|she (did|failed|chose)|they specifically)\b",
]
INSTITUTIONAL_AGENCY_MARKERS: list[str] = [
    r"\b(the system|the institution|the organization|the industry)\b",
    r"\b(designed to|structured to|built to|the machine)\b",
]
SYSTEMIC_AGENCY_MARKERS: list[str] = [
    r"\b(the fundamental|the architecture of|the paradigm)\b",
    r"\b(structural|systemic|the way society|deeply embedded)\b",
]


def _count_pattern_matches(text: str, patterns: list[str]) -> int:
    """Count total regex matches across a list of patterns."""
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def _find_passages_with_patterns(
    sentences: list[str],
    patterns: list[str],
    min_words: int = 0,
    label: str = "",
) -> list[EvidencePassage]:
    """Find sentences matching patterns and return as evidence passages."""
    passages: list[EvidencePassage] = []
    for idx, sent in enumerate(sentences):
        if min_words > 0 and len(sent.split()) < min_words:
            continue
        for pattern in patterns:
            if re.search(pattern, sent, re.IGNORECASE):
                passages.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label=label,
                ))
                break  # One match per sentence is enough
    return passages


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using basic regex."""
    # Split on sentence-ending punctuation followed by space or end
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _split_into_extended_passages(text: str, min_words: int = 200) -> list[str]:
    """Split text into extended passages of at least min_words.
    Groups consecutive sentences until word count threshold is met."""
    sentences = _split_into_sentences(text)
    passages: list[str] = []
    current: list[str] = []
    current_count = 0

    for sent in sentences:
        wc = len(sent.split())
        current.append(sent)
        current_count += wc
        if current_count >= min_words:
            passages.append(" ".join(current))
            current = []
            current_count = 0

    # Include final partial passage if it has substance
    if current and current_count >= min_words // 2:
        passages.append(" ".join(current))

    return passages


class AppraisalExtractor:
    """Extracts V1-V5 Cognitive Appraisal Variables from corpus.

    Spec §Phase 3: forensic passage analysis with Mandate 7 citation
    requirements. Each variable is extracted independently with
    evidence passage provenance.
    """

    def extract(
        self,
        corpus_text: str,
        triage_tier: TriageTier,
        session_id: str = "",
    ) -> AppraisalVariables:
        """Extract all applicable V1-V5 variables.

        Args:
            corpus_text: Full concatenated corpus text.
            triage_tier: Granularity tier from Phase 2.
            session_id: Source session ID for evidence provenance.

        Returns:
            AppraisalVariables with all extractable variables populated.
        """
        sentences = _split_into_sentences(corpus_text)
        passages = _split_into_extended_passages(corpus_text, V2_MINIMUM_PASSAGE_WORDS)
        result = AppraisalVariables()

        # V1: Always extractable at all tiers
        result.v1_trigger_specificity_threshold = self._extract_v1(
            sentences, corpus_text, session_id
        )

        # V2: Not extractable at LOW tier
        if triage_tier != TriageTier.LOW:
            result.v2_appraisal_sequence_ordering = self._extract_v2(
                passages, session_id
            )

        # V3: Always extractable at all tiers
        result.v3_coping_potential_pattern = self._extract_v3(
            sentences, session_id
        )

        # V4: Not extractable at LOW tier
        if triage_tier != TriageTier.LOW:
            result.v4_norm_compatibility_threshold = self._extract_v4(
                sentences, corpus_text, session_id
            )

        # V5: Always extractable at all tiers
        result.v5_agency_attribution_bias = self._extract_v5(
            sentences, session_id
        )

        return result

    def _extract_v1(
        self,
        sentences: list[str],
        corpus_text: str,
        session_id: str,
    ) -> V1TriggerSpecificityThreshold:
        """Spec §Phase 3 V1: Trigger Specificity Threshold.

        Extraction method: Identify all passages where the coach transitions
        from analytical/calm to emotionally activated. Measure the specificity
        of the activating stimulus. Calculate median specificity.
        """
        # Find activation passages
        activation_passages = _find_passages_with_patterns(
            sentences, ACTIVATION_MARKERS, label="activation_transition"
        )

        if len(activation_passages) < V1_MINIMUM_EVIDENCE_PASSAGES:
            return V1TriggerSpecificityThreshold()

        # Score specificity: count named entities, specific references
        # in each activation passage
        specificity_scores: list[int] = []
        for passage in activation_passages:
            score = self._score_stimulus_specificity(passage.passage_text)
            specificity_scores.append(score)
            passage.label = f"activation_specificity_{score}"
            passage.source_session_id = session_id

        # Calculate median
        sorted_scores = sorted(specificity_scores)
        n = len(sorted_scores)
        if n % 2 == 1:
            median = sorted_scores[n // 2]
        else:
            median = (sorted_scores[n // 2 - 1] + sorted_scores[n // 2]) // 2

        return V1TriggerSpecificityThreshold(
            score=max(1, min(10, median)),
            evidence_passages=activation_passages[:V1_MINIMUM_EVIDENCE_PASSAGES * 2],
        )

    def _score_stimulus_specificity(self, text: str) -> int:
        """Score the specificity of a trigger stimulus (1-10).

        Low (1-3): Generic stimuli ("the economy", "society")
        Medium (4-6): Domain-specific ("fee structures", "coaching industry")
        High (7-10): Precise mechanism ("the specific clause", named entities)
        """
        score = 3  # Baseline: generic

        # Named entities (proper nouns) → higher specificity
        proper_nouns = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
        if len(proper_nouns) >= 3:
            score += 3
        elif len(proper_nouns) >= 1:
            score += 1

        # Numbers, dates, specific references → higher specificity
        specific_refs = re.findall(
            r"\b(\d{4}|\d+%|section \d|clause|regulation|policy|rule \d)\b",
            text, re.IGNORECASE,
        )
        if specific_refs:
            score += 2

        # Domain jargon (multi-syllable technical words)
        long_words = [w for w in text.split() if len(w) > 10]
        if len(long_words) >= 3:
            score += 1

        return max(1, min(10, score))

    def _extract_v2(
        self,
        passages: list[str],
        session_id: str,
    ) -> V2AppraisalSequenceOrdering:
        """Spec §Phase 3 V2: Appraisal Sequence Ordering.

        Extraction method: Find 5+ extended passages (≥200 words).
        For each, label the first evaluative move.
        Calculate dominant pattern.
        """
        if len(passages) < V2_MINIMUM_PASSAGES:
            return V2AppraisalSequenceOrdering()

        # Classify each passage's first move
        move_counts: dict[str, int] = {
            "mechanism_first": 0,
            "moral_verdict_first": 0,
            "narrative_first": 0,
            "coping_first": 0,
        }
        evidence: list[EvidencePassage] = []

        for idx, passage in enumerate(passages):
            # Check first ~100 words for first move
            first_chunk = " ".join(passage.split()[:100])
            move = self._classify_first_move(first_chunk)
            move_counts[move] += 1
            evidence.append(EvidencePassage(
                passage_text=passage[:300] + ("..." if len(passage) > 300 else ""),
                passage_index=idx,
                label=move,
                source_session_id=session_id,
            ))

        total = sum(move_counts.values())
        if total == 0:
            return V2AppraisalSequenceOrdering()

        # Calculate percentages
        pct_breakdown = {k: round(v / total * 100, 1) for k, v in move_counts.items()}

        # Determine dominant type
        dominant_key = max(move_counts, key=lambda k: move_counts[k])
        dominant_count = move_counts[dominant_key]

        # If no clear dominant (e.g., distributed), mark as mixed
        if dominant_count / total < 0.4:
            seq_type = AppraisalSequenceType.MIXED
        else:
            type_map = {
                "mechanism_first": AppraisalSequenceType.MECHANISM_FIRST,
                "moral_verdict_first": AppraisalSequenceType.MORAL_VERDICT_FIRST,
                "narrative_first": AppraisalSequenceType.NARRATIVE_FIRST,
                "coping_first": AppraisalSequenceType.COPING_FIRST,
            }
            seq_type = type_map[dominant_key]

        return V2AppraisalSequenceOrdering(
            type=seq_type,
            percentage_breakdown=pct_breakdown,
            evidence_passages=evidence,
        )

    def _classify_first_move(self, text: str) -> str:
        """Classify the first evaluative move in a passage."""
        scores = {
            "mechanism_first": _count_pattern_matches(text, MECHANISM_FIRST_MARKERS),
            "moral_verdict_first": _count_pattern_matches(text, MORAL_VERDICT_FIRST_MARKERS),
            "narrative_first": _count_pattern_matches(text, NARRATIVE_FIRST_MARKERS),
            "coping_first": _count_pattern_matches(text, COPING_FIRST_MARKERS),
        }
        dominant = max(scores, key=lambda k: scores[k])
        if scores[dominant] == 0:
            return "mechanism_first"  # Default when no clear signal
        return dominant

    def _extract_v3(
        self,
        sentences: list[str],
        session_id: str,
    ) -> V3CopingPotentialPattern:
        """Spec §Phase 3 V3: Coping Potential Pattern.

        Extraction method: Classify passages as action or reflective.
        Score = action_count / (action_count + reflective_count).
        """
        action_passages = _find_passages_with_patterns(
            sentences, ACTION_INDICATORS, label="action"
        )
        reflective_passages = _find_passages_with_patterns(
            sentences, REFLECTIVE_INDICATORS, label="reflective"
        )

        action_count = len(action_passages)
        reflective_count = len(reflective_passages)
        total = action_count + reflective_count

        if total == 0 or (
            action_count < V3_MINIMUM_ACTION_PASSAGES
            and reflective_count < V3_MINIMUM_REFLECTIVE_PASSAGES
        ):
            return V3CopingPotentialPattern()

        ratio = round(action_count / total, 2) if total > 0 else 0.0

        for p in action_passages:
            p.source_session_id = session_id
        for p in reflective_passages:
            p.source_session_id = session_id

        combined_evidence = (
            action_passages[:V3_MINIMUM_ACTION_PASSAGES * 2]
            + reflective_passages[:V3_MINIMUM_REFLECTIVE_PASSAGES * 2]
        )

        return V3CopingPotentialPattern(
            ratio=ratio,
            action_count=action_count,
            reflective_count=reflective_count,
            evidence_passages=combined_evidence,
        )

    def _extract_v4(
        self,
        sentences: list[str],
        corpus_text: str,
        session_id: str,
    ) -> V4NormCompatibilityThreshold:
        """Spec §Phase 3 V4: Norm Compatibility Threshold.

        Extraction method: Identify passages with moral language.
        Rate severity of triggering violation. Map activation point.
        """
        moral_passages = _find_passages_with_patterns(
            sentences, MORAL_LANGUAGE_MARKERS, label="moral_language"
        )

        if len(moral_passages) < (V4_MINIMUM_OUTRAGE_PASSAGES + V4_MINIMUM_ANALYTICAL_PASSAGES):
            return V4NormCompatibilityThreshold()

        # Classify as outrage vs analytical-distance
        outrage_passages: list[EvidencePassage] = []
        analytical_passages: list[EvidencePassage] = []

        for passage in moral_passages:
            intensity = self._score_moral_intensity(passage.passage_text)
            if intensity >= 7:
                passage.label = f"outrage_intensity_{intensity}"
                outrage_passages.append(passage)
            else:
                passage.label = f"analytical_distance_{intensity}"
                analytical_passages.append(passage)
            passage.source_session_id = session_id

        if (
            len(outrage_passages) < V4_MINIMUM_OUTRAGE_PASSAGES
            or len(analytical_passages) < V4_MINIMUM_ANALYTICAL_PASSAGES
        ):
            # Not enough evidence for both sides
            if len(outrage_passages) >= V4_MINIMUM_OUTRAGE_PASSAGES:
                # Many outrage passages → low threshold
                score = 3
            elif len(analytical_passages) >= V4_MINIMUM_ANALYTICAL_PASSAGES:
                # Mostly analytical → high threshold
                score = 8
            else:
                return V4NormCompatibilityThreshold()
        else:
            # Calculate threshold from ratio
            outrage_ratio = len(outrage_passages) / (
                len(outrage_passages) + len(analytical_passages)
            )
            if outrage_ratio > 0.6:
                score = 3  # Low threshold — easy outrage
            elif outrage_ratio > 0.3:
                score = 5  # Medium threshold
            else:
                score = 8  # High threshold — rare outrage

        combined_evidence = (
            outrage_passages[:V4_MINIMUM_OUTRAGE_PASSAGES * 2]
            + analytical_passages[:V4_MINIMUM_ANALYTICAL_PASSAGES * 2]
        )

        return V4NormCompatibilityThreshold(
            score=score,
            evidence_passages=combined_evidence,
        )

    def _score_moral_intensity(self, text: str) -> int:
        """Score the moral intensity of a passage (1-10)."""
        intensity = 3  # baseline
        # High-intensity markers
        high_markers = re.findall(
            r"\b(furious|disgusting|criminal|evil|unforgivable|outrageous|betrayal)\b",
            text, re.IGNORECASE,
        )
        intensity += len(high_markers) * 2

        # Exclamation marks indicate emotional intensity
        intensity += text.count("!")

        # ALL CAPS words
        caps_words = re.findall(r"\b[A-Z]{3,}\b", text)
        intensity += len(caps_words)

        return max(1, min(10, intensity))

    def _extract_v5(
        self,
        sentences: list[str],
        session_id: str,
    ) -> V5AgencyAttributionBias:
        """Spec §Phase 3 V5: Agency Attribution Bias.

        Extraction method: Classify passages where coach attributes
        blame or credit. Count per category.
        """
        categories: dict[str, tuple[list[str], AgencyAttributionType]] = {
            "self": (SELF_AGENCY_MARKERS, AgencyAttributionType.SELF),
            "individual": (INDIVIDUAL_AGENCY_MARKERS, AgencyAttributionType.INDIVIDUAL),
            "institutional": (INSTITUTIONAL_AGENCY_MARKERS, AgencyAttributionType.INSTITUTIONAL),
            "systemic": (SYSTEMIC_AGENCY_MARKERS, AgencyAttributionType.SYSTEMIC),
        }

        distribution: dict[str, int] = {}
        all_evidence: list[EvidencePassage] = []

        for cat_name, (markers, _) in categories.items():
            passages = _find_passages_with_patterns(
                sentences, markers, label=f"agency_{cat_name}"
            )
            for p in passages:
                p.source_session_id = session_id
            distribution[cat_name] = len(passages)
            all_evidence.extend(passages[:5])

        total = sum(distribution.values())
        if total < V5_MINIMUM_ATTRIBUTION_PASSAGES:
            return V5AgencyAttributionBias()

        # Check minimum categories
        active_categories = sum(1 for v in distribution.values() if v > 0)
        if active_categories < V5_MINIMUM_CATEGORIES:
            return V5AgencyAttributionBias()

        # Determine dominant and secondary
        sorted_cats = sorted(distribution.items(), key=lambda x: x[1], reverse=True)
        dominant_key = sorted_cats[0][0]
        dominant_type = categories[dominant_key][1]

        secondary_type: Optional[AgencyAttributionType] = None
        if len(sorted_cats) > 1 and sorted_cats[1][1] > 0:
            secondary_count = sorted_cats[1][1]
            # Spec: "Record secondary if ≥25% of total"
            if total > 0 and secondary_count / total >= 0.25:
                secondary_key = sorted_cats[1][0]
                secondary_type = categories[secondary_key][1]

        return V5AgencyAttributionBias(
            dominant=dominant_type,
            secondary=secondary_type,
            distribution=distribution,
            evidence_passages=all_evidence,
        )
