"""
CCP FR5 Trigger Map Builder — Trigger Identifier Service (Unit 2)
Phase 2: Trigger identification using 6 LIWC-22 markers + V6-V10 MFT mapping.

Spec reference: FR5 Tech Spec §Phase 2
  - Uses 6 LIWC-22 markers: anger, anxiety, sadness, moral_outrage_proxy,
    authenticity, cognitive_processing
  - Cross-references V6-V10 moral foundation weights from DEP-LIB-001
  - Outputs: list of candidate TriggerEntry objects with moral foundation mapping

Research basis:
  Haidt MFQ-2 (2023) — moral foundation activation
  Pennebaker LIWC-22 — linguistic marker categories
"""

from typing import Optional

from src.ccp.models.emotional_dna_models import (
    EmotionalDNAProfile,
    MoralFoundations,
)
from src.ccp.models.trigger_map_models import (
    LIWC_22_TRIGGER_MARKERS,
    LIWC22MarkerScore,
    MoralFoundationMapping,
    MoralFoundationType,
    TriggerEntry,
    TriggerEvidencePassage,
)


class TriggerIdentifier:
    """Phase 2 service: Identifies triggers from corpus + emotional DNA.

    Scans corpus text for elevated LIWC-22 marker clusters, then maps
    each identified trigger to its primary/secondary moral foundation
    using the V6-V10 weights from DEP-LIB-001.

    Spec §Phase 2: 'Use 6 LIWC-22 markers to identify passages where
    the coach exhibits elevated emotional activation. Cross-reference
    with MFQ-2 moral foundations to determine which foundation is violated.'
    """

    # LIWC-22 keyword proxies for trigger detection
    # These are simplified proxies — production would use full LIWC-22 dictionaries
    LIWC_KEYWORD_SETS: dict[str, list[str]] = {
        "anger": [
            "angry", "furious", "outraged", "enraged", "livid", "infuriated",
            "frustrated", "irritated", "resentful", "hostile", "rage", "fury",
            "mad", "pissed", "seething", "disgusted", "appalled",
        ],
        "anxiety": [
            "anxious", "worried", "nervous", "fearful", "afraid", "terrified",
            "panicked", "dread", "uneasy", "tense", "stressed", "overwhelmed",
            "scared", "frightened", "alarmed", "distressed",
        ],
        "sadness": [
            "sad", "heartbroken", "devastated", "grief", "mourning", "loss",
            "despair", "hopeless", "miserable", "sorrowful", "dejected",
            "disappointed", "crushed", "distraught", "bereft",
        ],
        "moral_outrage_proxy": [
            "unfair", "unjust", "wrong", "immoral", "unethical", "corrupt",
            "violated", "betrayed", "exploited", "oppressed", "disgraceful",
            "shameful", "unacceptable", "intolerable", "unconscionable",
            "hypocritical", "fraudulent", "dishonest",
        ],
        "authenticity": [
            "i believe", "i know", "i feel", "i've seen", "i've lived",
            "my experience", "in my life", "personally", "genuinely",
            "honestly", "truthfully", "from my heart", "deep down",
        ],
        "cognitive_processing": [
            "because", "therefore", "realize", "understand", "recognize",
            "discovered", "learned", "figured out", "concluded", "reason",
            "insight", "epiphany", "awakening", "clarity", "transformed",
        ],
    }

    # Threshold for considering a marker elevated
    ELEVATION_THRESHOLD: float = 0.15

    # Minimum markers elevated to qualify as a trigger passage
    MINIMUM_ELEVATED_MARKERS: int = 2

    def identify(
        self,
        corpus_text: str,
        emotional_dna: EmotionalDNAProfile,
        session_id: str = "",
    ) -> list[TriggerEntry]:
        """Identify trigger candidates from corpus + emotional DNA.

        Args:
            corpus_text: Full corpus text to scan for trigger passages.
            emotional_dna: DEP-LIB-001 profile with V6-V10 moral foundations.
            session_id: Pipeline session identifier.

        Returns:
            List of TriggerEntry objects with moral foundation mapping populated.
        """
        # Step 1: Segment corpus into passages
        passages = self._segment_corpus(corpus_text)

        # Step 2: Score each passage on LIWC-22 markers
        scored_passages = []
        for idx, passage in enumerate(passages):
            scores = self._score_passage(passage, idx, session_id)
            elevated_count = sum(
                1 for s in scores if s.score >= self.ELEVATION_THRESHOLD
            )
            if elevated_count >= self.MINIMUM_ELEVATED_MARKERS:
                scored_passages.append((passage, idx, scores))

        # Step 3: Cluster adjacent elevated passages into trigger groups
        trigger_groups = self._cluster_passages(scored_passages)

        # Step 4: Map each trigger group to moral foundations
        triggers = []
        for group_idx, group in enumerate(trigger_groups):
            trigger = self._build_trigger_from_group(
                group=group,
                group_idx=group_idx,
                moral_foundations=emotional_dna.moral_foundations,
                session_id=session_id,
            )
            triggers.append(trigger)

        return triggers

    def _segment_corpus(self, corpus_text: str) -> list[str]:
        """Segment corpus into analysis passages.
        Uses paragraph-level segmentation (double newline split)
        with fallback to sentence-count chunking."""
        # Try paragraph split first
        paragraphs = [p.strip() for p in corpus_text.split("\n\n") if p.strip()]

        if len(paragraphs) >= 5:
            return paragraphs

        # Fallback: split by sentences, group into chunks of 3-5 sentences
        sentences = []
        for part in corpus_text.replace("!", ".").replace("?", ".").split("."):
            cleaned = part.strip()
            if cleaned:
                sentences.append(cleaned)

        if not sentences:
            return [corpus_text] if corpus_text.strip() else []

        # Group into passages of 3-5 sentences
        chunk_size = 4
        passages = []
        for i in range(0, len(sentences), chunk_size):
            chunk = ". ".join(sentences[i : i + chunk_size]) + "."
            passages.append(chunk)

        return passages

    def _score_passage(
        self, passage: str, passage_idx: int, session_id: str
    ) -> list[LIWC22MarkerScore]:
        """Score a single passage on all 6 LIWC-22 marker categories."""
        passage_lower = passage.lower()
        words = passage_lower.split()
        word_count = len(words) if words else 1

        scores = []
        for marker in LIWC_22_TRIGGER_MARKERS:
            keywords = self.LIWC_KEYWORD_SETS.get(marker, [])
            hit_count = 0
            for keyword in keywords:
                # Handle multi-word keywords
                if " " in keyword:
                    hit_count += passage_lower.count(keyword)
                else:
                    hit_count += sum(1 for w in words if keyword in w)

            # Normalize score by word count
            score = hit_count / word_count if word_count > 0 else 0.0

            evidence = []
            if hit_count > 0:
                evidence.append(
                    TriggerEvidencePassage(
                        passage_text=passage[:300],
                        source_session_id=session_id,
                        passage_index=passage_idx,
                        label=f"LIWC-22:{marker}",
                        confidence=min(score * 5, 1.0),  # scale for readability
                    )
                )

            scores.append(
                LIWC22MarkerScore(
                    marker=marker,
                    score=min(score, 1.0),
                    raw_count=hit_count,
                    evidence_passages=evidence,
                )
            )

        return scores

    def _cluster_passages(
        self, scored_passages: list[tuple[str, int, list[LIWC22MarkerScore]]]
    ) -> list[list[tuple[str, int, list[LIWC22MarkerScore]]]]:
        """Cluster adjacent elevated passages into trigger groups.
        Adjacent passages (index difference ≤ 2) are grouped together."""
        if not scored_passages:
            return []

        groups: list[list[tuple[str, int, list[LIWC22MarkerScore]]]] = []
        current_group: list[tuple[str, int, list[LIWC22MarkerScore]]] = [
            scored_passages[0]
        ]

        for i in range(1, len(scored_passages)):
            prev_idx = scored_passages[i - 1][1]
            curr_idx = scored_passages[i][1]

            if curr_idx - prev_idx <= 2:
                current_group.append(scored_passages[i])
            else:
                groups.append(current_group)
                current_group = [scored_passages[i]]

        groups.append(current_group)
        return groups

    def _build_trigger_from_group(
        self,
        group: list[tuple[str, int, list[LIWC22MarkerScore]]],
        group_idx: int,
        moral_foundations: MoralFoundations,
        session_id: str,
    ) -> TriggerEntry:
        """Build a TriggerEntry from a cluster of elevated passages."""
        # Collect all evidence passages
        all_evidence: list[TriggerEvidencePassage] = []
        dominant_markers: dict[str, float] = {}
        keywords_found: list[str] = []

        for passage_text, passage_idx, scores in group:
            for score_item in scores:
                if score_item.score >= self.ELEVATION_THRESHOLD:
                    # Accumulate marker scores
                    marker_name = score_item.marker
                    dominant_markers[marker_name] = dominant_markers.get(
                        marker_name, 0.0
                    ) + score_item.score

                    all_evidence.extend(score_item.evidence_passages)

                    # Extract keywords
                    for kw in self.LIWC_KEYWORD_SETS.get(marker_name, []):
                        if kw in passage_text.lower() and kw not in keywords_found:
                            keywords_found.append(kw)

        # Determine primary moral foundation from V6-V10 weights
        mft_mapping = self._map_to_moral_foundation(
            dominant_markers, moral_foundations
        )

        # Build the trigger entry
        trigger_id = f"trig_{group_idx + 1:03d}"
        combined_text = " ".join(p[0] for p in group)
        label = self._generate_trigger_label(
            dominant_markers, keywords_found, combined_text
        )

        return TriggerEntry(
            trigger_id=trigger_id,
            label=label,
            description=combined_text[:500],
            moral_foundation=mft_mapping,
            activation_keywords=keywords_found[:20],
            evidence_passages=all_evidence[:10],
        )

    def _map_to_moral_foundation(
        self,
        dominant_markers: dict[str, float],
        moral_foundations: MoralFoundations,
    ) -> MoralFoundationMapping:
        """Map LIWC-22 marker pattern to MFQ-2 moral foundation.

        Cross-references dominant emotional markers with V6-V10 weights
        to determine which moral foundation is being violated.
        """
        # Marker-to-foundation heuristic mapping
        marker_foundation_affinity: dict[str, list[MoralFoundationType]] = {
            "anger": [
                MoralFoundationType.FAIRNESS_CHEATING,
                MoralFoundationType.AUTHORITY_SUBVERSION,
            ],
            "anxiety": [
                MoralFoundationType.CARE_HARM,
                MoralFoundationType.SANCTITY_DEGRADATION,
            ],
            "sadness": [
                MoralFoundationType.CARE_HARM,
                MoralFoundationType.LOYALTY_BETRAYAL,
            ],
            "moral_outrage_proxy": [
                MoralFoundationType.FAIRNESS_CHEATING,
                MoralFoundationType.LIBERTY_OPPRESSION,
            ],
            "authenticity": [
                MoralFoundationType.SANCTITY_DEGRADATION,
                MoralFoundationType.CARE_HARM,
            ],
            "cognitive_processing": [
                MoralFoundationType.FAIRNESS_CHEATING,
                MoralFoundationType.AUTHORITY_SUBVERSION,
            ],
        }

        # Weight foundation candidates by marker scores * V6-V10 weights
        foundation_weights = moral_foundations.all_weights()
        foundation_scores: dict[MoralFoundationType, float] = {}

        for marker, score in dominant_markers.items():
            affinities = marker_foundation_affinity.get(marker, [])
            for foundation in affinities:
                # Get V6-V10 weight for this foundation
                v_weight = foundation_weights.get(foundation.value, 0.0) or 0.0
                combined = score * (1.0 + v_weight)  # boost by V6-V10 weight
                foundation_scores[foundation] = (
                    foundation_scores.get(foundation, 0.0) + combined
                )

        if not foundation_scores:
            return MoralFoundationMapping()

        # Sort by score descending
        sorted_foundations = sorted(
            foundation_scores.items(), key=lambda x: x[1], reverse=True
        )

        primary = sorted_foundations[0][0]
        secondary = sorted_foundations[1][0] if len(sorted_foundations) > 1 else None

        return MoralFoundationMapping(
            primary=primary,
            secondary=secondary,
        )

    def _generate_trigger_label(
        self,
        dominant_markers: dict[str, float],
        keywords: list[str],
        text: str,
    ) -> str:
        """Generate a human-readable label for the trigger.
        Format: '{dominant_marker} + {secondary_marker}: {keyword context}'."""
        if not dominant_markers:
            return "unclassified_trigger"

        sorted_markers = sorted(
            dominant_markers.items(), key=lambda x: x[1], reverse=True
        )
        top_marker = sorted_markers[0][0]

        # Use top keywords for context
        context_kws = keywords[:3]
        context_str = "_".join(context_kws) if context_kws else "general"

        return f"{top_marker}_{context_str}"
