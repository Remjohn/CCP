"""
CCP FR5 Trigger Map Builder — AKB Origin Classifier (Unit 3)
Phase 3: Conway AKB hierarchy classification with sensory anchor recording.

Spec reference: FR5 Tech Spec §Phase 3
  - Classify each trigger's originating experience into the Conway
    Autobiographical Knowledge Base hierarchy:
      * Lifetime Period (LP) — broad life chapter
      * General Event (GE) — repeated or extended event category
      * Event-Specific Knowledge (ESK) — single vivid episode with sensory trace
  - Record sensory anchors for ESK-level memories
  - ESK Test (Guardian Interview Phase 4): at least 3 responses contain
    sensory-perceptual detail

Research basis:
  Conway (2005) Self-Memory System — Autobiographical Knowledge Base hierarchy
  Tulving (1972) Episodic-Semantic Taxonomy
"""

from typing import Optional

from src.ccp.models.trigger_map_models import (
    AKBLevel,
    OriginClassification,
    SensoryAnchor,
    TriggerEntry,
    TriggerEvidencePassage,
)


class AKBOriginClassifier:
    """Phase 3 service: Classifies trigger origins using Conway AKB hierarchy.

    Each trigger's originating experience is classified as:
      - EVENT_SPECIFIC_KNOWLEDGE: vivid single episode with sensory traces
      - GENERAL_EVENT: repeated or extended event category
      - LIFETIME_PERIOD: broad life chapter context

    Conway (2005): The deeper the memory specificity, the more potent
    the trigger for content activation. ESK-level memories produce
    the strongest emotional transfer because they carry sensory-perceptual
    detail that enables audience neural coupling.
    """

    # Sensory modality keywords for detecting ESK-level detail
    SENSORY_MODALITY_KEYWORDS: dict[str, list[str]] = {
        "visual": [
            "saw", "looked", "watched", "stared", "noticed", "glanced",
            "bright", "dark", "color", "light", "shadow", "image",
            "face", "eyes", "picture", "scene",
        ],
        "auditory": [
            "heard", "listened", "sound", "voice", "noise", "whisper",
            "shout", "scream", "silence", "ring", "tone", "music",
            "said", "told", "words", "spoke",
        ],
        "olfactory": [
            "smell", "scent", "aroma", "stench", "fragrance", "odor",
            "perfume", "smoke", "chemical",
        ],
        "tactile": [
            "felt", "touched", "cold", "warm", "hot", "pressure",
            "pain", "tingling", "shaking", "trembling", "grip",
            "hand", "skin", "body",
        ],
        "gustatory": [
            "taste", "bitter", "sweet", "sour", "salty", "mouth",
            "tongue", "swallow", "nausea",
        ],
    }

    # Temporal specificity markers for ESK detection
    ESK_TEMPORAL_MARKERS: list[str] = [
        "that day", "that moment", "that night", "that morning",
        "i remember when", "the exact moment", "one time",
        "specifically", "on that particular", "at that exact",
        "i can still", "i'll never forget",
    ]

    # General event markers
    GE_MARKERS: list[str] = [
        "every time", "whenever", "always", "usually", "often",
        "repeatedly", "again and again", "kept happening",
        "for years", "throughout", "during that period",
        "in those days", "back then",
    ]

    # Lifetime period markers
    LP_MARKERS: list[str] = [
        "growing up", "childhood", "in my twenties", "in my thirties",
        "when i was young", "early career", "during college",
        "that phase of my life", "that chapter", "that era",
        "in school", "as a kid", "as a teenager",
    ]

    def classify(
        self, triggers: list[TriggerEntry], corpus_text: str, session_id: str = ""
    ) -> list[TriggerEntry]:
        """Classify each trigger's originating experience using Conway AKB.

        Args:
            triggers: List of TriggerEntry objects from Phase 2.
            corpus_text: Full corpus for contextual classification.
            session_id: Pipeline session identifier.

        Returns:
            Same triggers with originating_experience populated.
        """
        for trigger in triggers:
            origin = self._classify_single_trigger(trigger, corpus_text, session_id)
            trigger.originating_experience = origin

        return triggers

    def _classify_single_trigger(
        self, trigger: TriggerEntry, corpus_text: str, session_id: str
    ) -> OriginClassification:
        """Classify a single trigger's origin in the AKB hierarchy."""
        # Use trigger's evidence passages for primary classification
        evidence_text = " ".join(
            ep.passage_text for ep in trigger.evidence_passages
        )
        if not evidence_text:
            evidence_text = trigger.description

        text_lower = evidence_text.lower()

        # Score each AKB level
        esk_score = self._score_esk(text_lower)
        ge_score = self._score_ge(text_lower)
        lp_score = self._score_lp(text_lower)

        # Determine AKB level
        if esk_score > ge_score and esk_score > lp_score:
            akb_level = AKBLevel.EVENT_SPECIFIC_KNOWLEDGE
        elif ge_score > lp_score:
            akb_level = AKBLevel.GENERAL_EVENT
        else:
            akb_level = AKBLevel.LIFETIME_PERIOD

        # Extract sensory anchors (especially for ESK)
        sensory_anchors = self._extract_sensory_anchors(
            text_lower, evidence_text, session_id
        )

        # Extract temporal context
        temporal_context = self._extract_temporal_context(text_lower)

        # Build evidence passages for classification
        classification_evidence = [
            TriggerEvidencePassage(
                passage_text=evidence_text[:300],
                source_session_id=session_id,
                label=f"AKB:{akb_level.value}",
                confidence=max(esk_score, ge_score, lp_score),
            )
        ]

        return OriginClassification(
            akb_level=akb_level,
            narrative_summary=trigger.description[:500],
            sensory_anchors=sensory_anchors,
            temporal_context=temporal_context,
            evidence_passages=classification_evidence,
        )

    def _score_esk(self, text_lower: str) -> float:
        """Score text for Event-Specific Knowledge indicators.
        ESK = vivid single episode with sensory traces."""
        score = 0.0

        # Temporal specificity markers
        for marker in self.ESK_TEMPORAL_MARKERS:
            if marker in text_lower:
                score += 0.15

        # Sensory detail presence
        for modality, keywords in self.SENSORY_MODALITY_KEYWORDS.items():
            modality_hits = sum(1 for kw in keywords if kw in text_lower)
            if modality_hits > 0:
                score += 0.1 * min(modality_hits, 3)

        # First-person vivid narration indicators
        vivid_markers = [
            "i remember", "i can see", "i can hear", "i can feel",
            "i was standing", "i was sitting", "i looked",
        ]
        for marker in vivid_markers:
            if marker in text_lower:
                score += 0.1

        return min(score, 1.0)

    def _score_ge(self, text_lower: str) -> float:
        """Score text for General Event indicators.
        GE = repeated or extended event category."""
        score = 0.0
        for marker in self.GE_MARKERS:
            if marker in text_lower:
                score += 0.15
        return min(score, 1.0)

    def _score_lp(self, text_lower: str) -> float:
        """Score text for Lifetime Period indicators.
        LP = broad life chapter context."""
        score = 0.0
        for marker in self.LP_MARKERS:
            if marker in text_lower:
                score += 0.15
        return min(score, 1.0)

    def _extract_sensory_anchors(
        self, text_lower: str, original_text: str, session_id: str
    ) -> list[SensoryAnchor]:
        """Extract sensory-perceptual detail anchors from text.
        Conway AKB: ESK includes sensory traces that enable re-experiencing."""
        anchors: list[SensoryAnchor] = []

        for modality, keywords in self.SENSORY_MODALITY_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in text_lower]
            if hits:
                # Find the surrounding context for the first hit
                first_hit = hits[0]
                hit_pos = text_lower.find(first_hit)
                context_start = max(0, hit_pos - 50)
                context_end = min(len(original_text), hit_pos + len(first_hit) + 50)
                context = original_text[context_start:context_end].strip()

                evidence = TriggerEvidencePassage(
                    passage_text=context,
                    source_session_id=session_id,
                    label=f"sensory:{modality}",
                    confidence=min(len(hits) * 0.2, 1.0),
                )

                anchors.append(
                    SensoryAnchor(
                        modality=modality,
                        description=context,
                        evidence_passage=evidence,
                    )
                )

        return anchors

    def _extract_temporal_context(self, text_lower: str) -> str:
        """Extract temporal context from text for the trigger origin."""
        # Check for specific temporal references
        all_markers = (
            self.ESK_TEMPORAL_MARKERS + self.GE_MARKERS + self.LP_MARKERS
        )
        found = [m for m in all_markers if m in text_lower]
        if found:
            return f"Temporal markers found: {', '.join(found[:5])}"
        return ""
