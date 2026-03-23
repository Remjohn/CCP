"""
CCP FR5 Trigger Map Builder — Reconsolidation Scorer (Unit 6)
Phase 6: Nader reconsolidation sensitivity scoring with V1 cross-validation.

Spec reference: FR5 Tech Spec §Phase 6
  - Score each trigger's reconsolidation sensitivity on a 1-10 scale:
      * 1 = easily labilized (low prediction error needed)
      * 10 = requires high specificity to labilize
  - Cross-validate against V1 (Trigger Specificity Threshold from DEP-LIB-001)
  - AC7: 'Reconsolidation sensitivity score is cross-validated against
    V1 Trigger Specificity Threshold'

Research basis:
  Nader, Schafe & Le Doux (2000) — Memory Reconsolidation
  Nader (2003) — Fear memories require protein synthesis for reconsolidation
  Schiller et al. (2010) — Prediction error window for reconsolidation
"""

from typing import Optional

from src.ccp.models.emotional_dna_models import EmotionalDNAProfile
from src.ccp.models.trigger_map_models import (
    RECONSOLIDATION_MAX,
    RECONSOLIDATION_MIN,
    ReconsolidationSensitivity,
    TriggerEntry,
    TriggerEvidencePassage,
)


class ReconsolidationScorer:
    """Phase 6 service: Scores reconsolidation sensitivity per trigger.

    Nader et al. (2000): When a consolidated memory is reactivated,
    it enters a labile state where it can be modified (reconsolidated).
    The prediction error threshold is the minimum surprise required
    to open the reconsolidation window for a given memory trace.

    Higher scores (8-10) = deeply consolidated memories that require
    highly specific, novel information to labilize.
    Lower scores (1-3) = easily labilized memories that respond to
    general emotional activation.

    Cross-validation with V1 (Trigger Specificity Threshold):
    High V1 score (high specificity) should correlate with high
    reconsolidation sensitivity (harder to labilize with generic input).
    """

    # Consolidation depth markers (suggest high reconsolidation threshold)
    HIGH_CONSOLIDATION_MARKERS: list[str] = [
        "i've always known", "it's fundamental", "core belief",
        "non-negotiable", "this defines me", "always been this way",
        "deeply ingrained", "part of my identity",
        "i'll never change on this", "my life's work",
        "this is who i am", "i've dedicated my life",
    ]

    # Lability markers (suggest low reconsolidation threshold)
    HIGH_LABILITY_MARKERS: list[str] = [
        "i'm starting to question", "maybe i was wrong",
        "i'm reconsidering", "i used to think but now",
        "someone showed me", "i hadn't considered",
        "my perspective shifted", "i'm evolving on this",
        "i'm open to", "i recently realized",
    ]

    # Emotional entrenchment markers (moderate-high threshold)
    ENTRENCHMENT_MARKERS: list[str] = [
        "every time i see", "it triggers me",
        "i can't help but react", "automatic response",
        "visceral reaction", "gut response",
        "knee-jerk", "instant anger",
    ]

    # Maximum allowed divergence between V1 and reconsolidation score
    V1_CROSS_VALIDATION_MAX_DIVERGENCE: int = 3

    def score(
        self,
        triggers: list[TriggerEntry],
        emotional_dna: EmotionalDNAProfile,
        corpus_text: str,
        session_id: str = "",
    ) -> list[TriggerEntry]:
        """Score reconsolidation sensitivity for each trigger.

        Args:
            triggers: List of TriggerEntry objects from Phase 5.
            emotional_dna: DEP-LIB-001 profile for V1 cross-validation.
            corpus_text: Full corpus for contextual scoring.
            session_id: Pipeline session identifier.

        Returns:
            Same triggers with reconsolidation_sensitivity populated.
        """
        # Get V1 score for cross-validation
        v1_score = self._get_v1_score(emotional_dna)

        for trigger in triggers:
            sensitivity = self._score_single_trigger(
                trigger, v1_score, corpus_text, session_id
            )
            trigger.reconsolidation_sensitivity = sensitivity

        return triggers

    def _get_v1_score(self, emotional_dna: EmotionalDNAProfile) -> Optional[int]:
        """Extract V1 Trigger Specificity Threshold from DEP-LIB-001."""
        v1 = emotional_dna.appraisal_variables.v1_trigger_specificity_threshold
        return v1.score if v1.is_populated() else None

    def _score_single_trigger(
        self,
        trigger: TriggerEntry,
        v1_score: Optional[int],
        corpus_text: str,
        session_id: str,
    ) -> ReconsolidationSensitivity:
        """Score a single trigger's reconsolidation sensitivity.

        Nader (2000): The prediction error threshold depends on how
        deeply consolidated the memory trace is. More rehearsed,
        emotionally intense, and identity-central memories require
        higher prediction error to open the reconsolidation window.
        """
        evidence_text = " ".join(
            ep.passage_text for ep in trigger.evidence_passages
        )
        context = f"{evidence_text} {trigger.description}".lower()

        # Score consolidation depth
        high_score = self._score_markers(context, self.HIGH_CONSOLIDATION_MARKERS)
        low_score = self._score_markers(context, self.HIGH_LABILITY_MARKERS)
        entrenchment_score = self._score_markers(
            context, self.ENTRENCHMENT_MARKERS
        )

        # Calculate base score (1-10)
        # High consolidation + entrenchment → higher score
        # High lability → lower score
        base_score = 5.0  # neutral starting point
        base_score += high_score * 3.0  # consolidated memories push up
        base_score += entrenchment_score * 2.0  # entrenchment pushes up
        base_score -= low_score * 3.0  # lability pushes down

        # Clamp to 1-10
        raw_score = max(
            RECONSOLIDATION_MIN,
            min(RECONSOLIDATION_MAX, round(base_score)),
        )

        # Cross-validate against V1
        v1_validated = False
        v1_score_at_validation = v1_score

        if v1_score is not None:
            divergence = abs(raw_score - v1_score)
            if divergence <= self.V1_CROSS_VALIDATION_MAX_DIVERGENCE:
                v1_validated = True
            else:
                # Adjust toward V1 if divergence is too high
                # V1 Trigger Specificity and reconsolidation sensitivity
                # should be correlated — high specificity = harder to labilize
                adjustment_direction = 1 if v1_score > raw_score else -1
                raw_score = raw_score + adjustment_direction * (
                    divergence - self.V1_CROSS_VALIDATION_MAX_DIVERGENCE
                )
                raw_score = max(
                    RECONSOLIDATION_MIN,
                    min(RECONSOLIDATION_MAX, round(raw_score)),
                )
                v1_validated = True

        evidence = [
            TriggerEvidencePassage(
                passage_text=context[:300],
                source_session_id=session_id,
                label=f"reconsolidation:score={raw_score}",
                confidence=0.7 if v1_validated else 0.5,
            )
        ]

        return ReconsolidationSensitivity(
            score=raw_score,
            v1_cross_validated=v1_validated,
            v1_score_at_validation=v1_score_at_validation,
            evidence_passages=evidence,
        )

    def _score_markers(self, text: str, markers: list[str]) -> float:
        """Score text against a list of markers. Returns 0.0-1.0."""
        if not text:
            return 0.0
        hit_count = sum(1 for marker in markers if marker in text)
        return min(hit_count * 0.12, 1.0)
