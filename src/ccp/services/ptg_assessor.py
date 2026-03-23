"""
CCP FR5 Trigger Map Builder — PTG Assessor (Unit 4)
Phase 4: Tedeschi & Calhoun PTG assessment with HARD EXCLUDE safety gate.

Spec reference: FR5 Tech Spec §Phase 4
  - Assess each trigger's post-traumatic growth status:
      * resolved_dual_layer — path out fully encoded, can access both
        original pain AND resolution simultaneously
      * active_processing — partial resolution, still developing
      * raw_unresolved — live trauma, NOT suitable for content activation
  - HARD EXCLUDE: raw_unresolved triggers are filtered at CODE LEVEL
    (not prompt level). This is AC2.
  - Spec: 'The safety gate is implemented as a hard code-level filter,
    not a prompt instruction. raw_unresolved triggers are NEVER emitted
    to triggers[] — they are excluded entirely.'

Research basis:
  Tedeschi & Calhoun (2004) Posttraumatic Growth Inventory
"""

from typing import Optional

from src.ccp.models.trigger_map_models import (
    PTGAssessment,
    PTGStatus,
    TriggerEntry,
    TriggerEvidencePassage,
)


class PTGAssessor:
    """Phase 4 service: Assesses PTG status for each trigger.

    Implements the Tedeschi & Calhoun (2004) three-tier classification
    with the HARD EXCLUDE safety gate for raw_unresolved triggers.

    The safety gate is AC2: 'raw_unresolved triggers are never emitted
    into triggers[]. They appear NOWHERE in the output. This is a
    code-level filter, not a prompt-level instruction.'
    """

    # Markers indicating resolved_dual_layer (can access both pain + resolution)
    RESOLVED_MARKERS: list[str] = [
        "i've learned", "looking back", "i now understand",
        "that experience taught me", "i'm grateful",
        "it made me who i am", "i grew from",
        "i can see now", "the gift was", "i wouldn't change",
        "it was painful but", "through that pain",
        "i found strength", "i discovered", "i transformed",
        "on the other side", "i came through",
        "i've healed", "i've processed", "i've made peace",
    ]

    # Markers indicating active_processing (partial resolution)
    ACTIVE_PROCESSING_MARKERS: list[str] = [
        "i'm still working through", "i'm learning to",
        "it's getting better", "i'm starting to see",
        "i haven't fully", "still processing",
        "i'm in the process", "coming to terms",
        "some days are harder", "it's a journey",
        "i'm beginning to", "slowly understanding",
        "not there yet", "making progress",
    ]

    # Markers indicating raw_unresolved (live trauma — EXCLUDE)
    RAW_UNRESOLVED_MARKERS: list[str] = [
        "i can't talk about", "it still hurts too much",
        "i'm not ready", "it's too raw",
        "i can't go there", "it destroys me",
        "i break down", "i can't breathe when",
        "i still have nightmares", "i'm still traumatized",
        "i haven't been able to", "it's like it just happened",
        "i freeze when", "i can't function",
        "it haunts me", "i'm still in crisis",
    ]

    def assess(
        self,
        triggers: list[TriggerEntry],
        corpus_text: str,
        session_id: str = "",
    ) -> tuple[list[TriggerEntry], list[TriggerEntry], list[TriggerEntry]]:
        """Assess PTG status for each trigger and partition into categories.

        HARD EXCLUDE: raw_unresolved triggers are separated at code level.
        They are NEVER included in the resolved or candidate lists.

        Args:
            triggers: List of TriggerEntry objects from Phase 3.
            corpus_text: Full corpus for contextual assessment.
            session_id: Pipeline session identifier.

        Returns:
            Tuple of (resolved_triggers, active_triggers, excluded_triggers).
            - resolved_triggers: PTG status = resolved_dual_layer
            - active_triggers: PTG status = active_processing
            - excluded_triggers: PTG status = raw_unresolved (EXCLUDED)
        """
        resolved: list[TriggerEntry] = []
        active: list[TriggerEntry] = []
        excluded: list[TriggerEntry] = []

        for trigger in triggers:
            assessment = self._assess_single_trigger(
                trigger, corpus_text, session_id
            )
            trigger.ptg_status = assessment

            # HARD CODE-LEVEL FILTER — AC2 enforcement
            if assessment.status == PTGStatus.RAW_UNRESOLVED:
                # raw_unresolved = HARD EXCLUDE
                # These triggers appear NOWHERE in the output
                excluded.append(trigger)
            elif assessment.status == PTGStatus.RESOLVED_DUAL_LAYER:
                resolved.append(trigger)
            else:
                # active_processing → candidate_triggers[]
                active.append(trigger)

        return resolved, active, excluded

    def _assess_single_trigger(
        self, trigger: TriggerEntry, corpus_text: str, session_id: str
    ) -> PTGAssessment:
        """Assess PTG status for a single trigger.

        Tedeschi & Calhoun (2004):
        - resolved_dual_layer: Can access both original pain AND resolution.
          The coach can tell the story of the wound AND the path out.
        - active_processing: Partial resolution. The coach is working through
          it but hasn't fully encoded the dual-layer access.
        - raw_unresolved: Live trauma. No resolution signal present.
          MUST be excluded from content activation.
        """
        # Use trigger evidence + full corpus context
        evidence_text = " ".join(
            ep.passage_text for ep in trigger.evidence_passages
        )
        context_text = f"{evidence_text} {trigger.description}".lower()

        # Score each PTG category
        resolved_score = self._score_markers(context_text, self.RESOLVED_MARKERS)
        active_score = self._score_markers(
            context_text, self.ACTIVE_PROCESSING_MARKERS
        )
        raw_score = self._score_markers(context_text, self.RAW_UNRESOLVED_MARKERS)

        # Determine status (highest score wins, with safety bias)
        # Safety bias: if raw_unresolved has ANY signal, it takes priority
        # over active_processing (but not over strong resolved signal)
        if raw_score > 0 and resolved_score < 0.3:
            status = PTGStatus.RAW_UNRESOLVED
            resolution_signal = "Raw trauma markers detected — EXCLUDED"
        elif resolved_score > active_score and resolved_score > raw_score:
            status = PTGStatus.RESOLVED_DUAL_LAYER
            resolution_signal = "Dual-layer resolution signals present"
        elif active_score > 0:
            status = PTGStatus.ACTIVE_PROCESSING
            resolution_signal = "Active processing markers detected"
        else:
            # Default: active_processing (safer than resolved, not excluded)
            status = PTGStatus.ACTIVE_PROCESSING
            resolution_signal = "Insufficient signal — classified as active processing"

        evidence = [
            TriggerEvidencePassage(
                passage_text=context_text[:300],
                source_session_id=session_id,
                label=f"PTG:{status.value}",
                confidence=max(resolved_score, active_score, raw_score),
            )
        ]

        return PTGAssessment(
            status=status,
            resolution_signal=resolution_signal,
            evidence_passages=evidence,
        )

    def _score_markers(self, text: str, markers: list[str]) -> float:
        """Score text against a list of markers. Returns 0.0-1.0."""
        if not text:
            return 0.0

        hit_count = sum(1 for marker in markers if marker in text)
        # Normalize: each hit adds 0.15, cap at 1.0
        return min(hit_count * 0.15, 1.0)
