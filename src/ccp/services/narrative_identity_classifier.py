"""
CCP FR5 Trigger Map Builder — Narrative Identity Classifier (Unit 5)
Phase 5: McAdams narrative identity classification.

Spec reference: FR5 Tech Spec §Phase 5
  - Classify each trigger's narrative sequence type:
      * redemption — negative → positive transformation
      * contamination — positive → negative deterioration
      * mixed — both elements present without clear dominance
  - Classify positioning (how the coach positions themselves):
      * reluctant_hero — didn't seek the fight, but answered the call
      * whistleblower — exposes what others won't
      * reformed_insider — was part of the problem, now fights it
      * outsider_witness — sees the pattern others can't
      * survivor_guide — came through it, now leads others

Research basis:
  McAdams (2001) Narrative Identity — The Redemptive Self
  McAdams & McLean (2013) Narrative Identity
"""

from typing import Optional

from src.ccp.models.trigger_map_models import (
    NarrativeIdentityClassification,
    NarrativePositioning,
    NarrativeSequenceType,
    TriggerEntry,
    TriggerEvidencePassage,
)


class NarrativeIdentityClassifier:
    """Phase 5 service: Classifies narrative identity for each trigger.

    McAdams (2001): People construct internalized, evolving life stories
    that integrate reconstructed past, perceived present, and imagined
    future. The key dimension is whether the narrative follows a
    redemption arc (bad → good) or contamination arc (good → bad).

    The positioning classification determines how the coach positions
    themselves in relation to the trigger — this directly affects
    which script archetypes can authentically activate the trigger.
    """

    # Redemption sequence markers (negative → positive transformation)
    REDEMPTION_MARKERS: list[str] = [
        "but then", "everything changed when", "that's when i realized",
        "the turning point was", "it led me to", "from that pain",
        "because of that", "it transformed me", "i found my purpose",
        "it gave me", "silver lining", "blessing in disguise",
        "made me stronger", "opened my eyes", "freed me",
        "i discovered my calling", "that pain became my fuel",
    ]

    # Contamination sequence markers (positive → negative deterioration)
    CONTAMINATION_MARKERS: list[str] = [
        "everything fell apart", "it all went wrong",
        "that's when things got dark", "i lost everything",
        "it was taken from me", "destroyed", "shattered",
        "the betrayal", "it poisoned", "it corrupted",
        "what started as good", "turned toxic",
        "i was naive to think", "the illusion shattered",
    ]

    # Reluctant hero positioning markers
    RELUCTANT_HERO_MARKERS: list[str] = [
        "i never wanted to", "i didn't choose this fight",
        "someone had to", "i couldn't just stand by",
        "i was forced to", "reluctantly", "not my fight but",
        "i had to step up", "couldn't look away",
    ]

    # Whistleblower positioning markers
    WHISTLEBLOWER_MARKERS: list[str] = [
        "nobody talks about", "the industry doesn't want you to know",
        "i'm going to say what", "the truth is",
        "everyone's afraid to say", "i'll be the one to",
        "expose", "reveal", "uncover", "call out",
        "someone needs to tell the truth", "dirty secret",
    ]

    # Reformed insider positioning markers
    REFORMED_INSIDER_MARKERS: list[str] = [
        "i used to be part of", "i was that person",
        "i did the same thing", "i was complicit",
        "i know because i was inside", "former",
        "i changed when", "i left because", "i couldn't anymore",
        "i was the problem", "i've been on both sides",
    ]

    # Outsider witness positioning markers
    OUTSIDER_WITNESS_MARKERS: list[str] = [
        "i've always seen", "from the outside",
        "watching people", "i noticed a pattern",
        "what nobody else sees", "the bigger picture",
        "step back and look", "perspective",
        "i observe", "i see what others miss",
    ]

    # Survivor guide positioning markers
    SURVIVOR_GUIDE_MARKERS: list[str] = [
        "i went through", "i survived", "i came out the other side",
        "i can show you", "because i've been there",
        "i know the path", "i've walked that road",
        "my scars are my map", "i can guide you",
        "i've done the work", "been in your shoes",
    ]

    def classify(
        self, triggers: list[TriggerEntry], corpus_text: str, session_id: str = ""
    ) -> list[TriggerEntry]:
        """Classify narrative identity for each trigger.

        Args:
            triggers: List of TriggerEntry objects from Phase 4.
            corpus_text: Full corpus for contextual classification.
            session_id: Pipeline session identifier.

        Returns:
            Same triggers with narrative_identity populated.
        """
        for trigger in triggers:
            classification = self._classify_single_trigger(
                trigger, corpus_text, session_id
            )
            trigger.narrative_identity = classification

        return triggers

    def _classify_single_trigger(
        self, trigger: TriggerEntry, corpus_text: str, session_id: str
    ) -> NarrativeIdentityClassification:
        """Classify a single trigger's narrative identity."""
        evidence_text = " ".join(
            ep.passage_text for ep in trigger.evidence_passages
        )
        context = f"{evidence_text} {trigger.description}".lower()

        # Determine sequence type
        sequence_type = self._classify_sequence(context)

        # Determine positioning
        positioning = self._classify_positioning(context)

        evidence = [
            TriggerEvidencePassage(
                passage_text=context[:300],
                source_session_id=session_id,
                label=f"narrative:{sequence_type.value}_{positioning.value}",
                confidence=0.7,
            )
        ]

        return NarrativeIdentityClassification(
            sequence_type=sequence_type,
            positioning=positioning,
            evidence_passages=evidence,
        )

    def _classify_sequence(self, text: str) -> NarrativeSequenceType:
        """Classify the narrative sequence type.

        McAdams (2001):
        - Redemption: negative experience → positive outcome
        - Contamination: positive state → negative outcome
        - Mixed: both patterns present, no clear dominance
        """
        redemption_score = self._score_markers(text, self.REDEMPTION_MARKERS)
        contamination_score = self._score_markers(text, self.CONTAMINATION_MARKERS)

        # Both present at similar levels = mixed
        if (
            redemption_score > 0
            and contamination_score > 0
            and abs(redemption_score - contamination_score) < 0.15
        ):
            return NarrativeSequenceType.MIXED

        if redemption_score > contamination_score:
            return NarrativeSequenceType.REDEMPTION
        elif contamination_score > redemption_score:
            return NarrativeSequenceType.CONTAMINATION
        else:
            # Default to mixed when insufficient signal
            return NarrativeSequenceType.MIXED

    def _classify_positioning(self, text: str) -> NarrativePositioning:
        """Classify the narrator's positioning relative to the trigger.

        This determines which script archetypes can authentically
        activate this trigger — a whistleblower trigger maps differently
        than a survivor guide trigger in the Trigger-First Engine.
        """
        positioning_scores: dict[NarrativePositioning, float] = {
            NarrativePositioning.RELUCTANT_HERO: self._score_markers(
                text, self.RELUCTANT_HERO_MARKERS
            ),
            NarrativePositioning.WHISTLEBLOWER: self._score_markers(
                text, self.WHISTLEBLOWER_MARKERS
            ),
            NarrativePositioning.REFORMED_INSIDER: self._score_markers(
                text, self.REFORMED_INSIDER_MARKERS
            ),
            NarrativePositioning.OUTSIDER_WITNESS: self._score_markers(
                text, self.OUTSIDER_WITNESS_MARKERS
            ),
            NarrativePositioning.SURVIVOR_GUIDE: self._score_markers(
                text, self.SURVIVOR_GUIDE_MARKERS
            ),
        }

        # Find highest scoring positioning
        best_positioning = max(positioning_scores, key=positioning_scores.get)  # type: ignore[arg-type]
        best_score = positioning_scores[best_positioning]

        # Default to survivor_guide when insufficient signal
        # (most common coaching positioning)
        if best_score == 0:
            return NarrativePositioning.SURVIVOR_GUIDE

        return best_positioning

    def _score_markers(self, text: str, markers: list[str]) -> float:
        """Score text against a list of markers. Returns 0.0-1.0."""
        if not text:
            return 0.0
        hit_count = sum(1 for marker in markers if marker in text)
        return min(hit_count * 0.12, 1.0)
