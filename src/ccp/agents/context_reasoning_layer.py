"""
CCP Context Reasoning Layer — FR1 Unit 9
DEP-ENG-025: 3-Question Context Reasoning Layer (Research Planner V4.0 Pre-Compilation)

Spec reference: FR1 Tech Spec §Step 11-B, DEP-ENG-025
Architecture reference: CCP_Technical_Architecture.md §3.2

The Context Reasoning Layer runs BEFORE every script generation call.
It answers 3 questions to populate the ContextSelectionObject (DEP-ENG-025):

  Q1: Story Archive eligibility — M4 RESONANT story present? (AC5)
  Q2: CMM layer performance weighting — which layer has best performance history?
  Q3: Humor mechanism precedent — any mechanism used in last 8 weeks?

Output: ContextSelectionObject → written to context_performance_registry.

C-11 Persona Masking Gate: no agent names in model-facing prompts.
"""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from src.ccp.models.v5_models import (
    ContextSelectionObject,
    ContextPerformanceRegistry,
    CulturalMemoryMap,
    CMMLayerType,
    CoachStoryArchive,
    HumorMechanismRegistry,
)


class ContextReasoningLayer:
    """DEP-ENG-025: 3-Question Context Reasoning Layer.

    Spec: 'Research Planner V4.0 pre-compilation sequence'

    Executed before every content generation batch to select the appropriate:
    - Story archive entry (if M4 RESONANT moment)
    - CMM layer reference (highest performance weight)
    - Humor mechanism (precedent check, Boredom Ban enforcement)

    Output is a ContextSelectionObject stored in context_performance_registry.
    """

    def __init__(
        self,
        coach_id: str,
        coach_acronym: str,
        coach_dir: Path,
    ):
        self.coach_id = coach_id
        self.coach_acronym = coach_acronym.upper()
        self.coach_dir = coach_dir

    # -------------------------------------------------------------------------
    # Q1: Story Archive Eligibility (AC5)
    # -------------------------------------------------------------------------

    def _q1_story_archive_check(
        self,
        story_archive: CoachStoryArchive,
        session_cral_phase: str,
    ) -> tuple[bool, Optional[str]]:
        """Q1: Should a story archive entry be surfaced for this session?

        AC5: 'Context Reasoning Layer Q1 surfaces story_archive_used: true
        when a RESONANT-phase story is present and the session is M4.'

        Args:
            story_archive: The coach's confirmed story archive.
            session_cral_phase: The CRAL phase for the current session
                                (e.g., "M4_RESONANT").

        Returns:
            Tuple of (story_used: bool, story_id_selected: Optional[str])
        """
        if session_cral_phase != "M4_RESONANT":
            return False, None

        # Query stories that fit M4 RESONANT
        resonant_stories = story_archive.query_by_cral_moment("M4_RESONANT")
        if not resonant_stories:
            return False, None

        # Prefer client_breakthrough or personal_transformation for M4
        preferred_types = ["client_breakthrough", "personal_transformation"]
        for story in resonant_stories:
            if story.story_type.value in preferred_types:
                return True, story.story_id

        # Fall back to first available
        return True, resonant_stories[0].story_id

    # -------------------------------------------------------------------------
    # Q2: CMM Layer Performance Weighting
    # -------------------------------------------------------------------------

    def _q2_cmm_layer_weighting(
        self,
        cmm: CulturalMemoryMap,
        performance_registry: ContextPerformanceRegistry,
    ) -> Optional[str]:
        """Q2: Which CMM layer has the best performance history for this coach?

        Looks up session_history in the ContextPerformanceRegistry to find
        the CMM layer with the highest average engagement score.

        Falls back to INDUSTRY_MYTHOLOGY (Layer 3) as the default highest-value
        layer for new coaches with no performance history.

        Args:
            cmm: The coach's confirmed Cultural Memory Map.
            performance_registry: The context performance registry.

        Returns:
            The CMM layer type value string (e.g., 'industry_mythology').
        """
        if not performance_registry.session_history:
            # Default: Layer 3 Industry Mythology has highest new-audience signal value
            # (per CMM spec — industry challenges generate most resonance)
            populated_layers = [
                e.layer_type.value for e in cmm.entries
                if e.operator_approved
            ]
            if CMMLayerType.INDUSTRY_MYTHOLOGY.value in populated_layers:
                return CMMLayerType.INDUSTRY_MYTHOLOGY.value
            # Fall to first populated layer
            return populated_layers[0] if populated_layers else None

        # Aggregate performance by CMM layer
        layer_scores: dict[str, list[float]] = {}
        for session in performance_registry.session_history:
            layer = session.get("cmm_layer_used")
            score = session.get("engagement_score", 0.0)
            if layer:
                if layer not in layer_scores:
                    layer_scores[layer] = []
                layer_scores[layer].append(score)

        if not layer_scores:
            return CMMLayerType.INDUSTRY_MYTHOLOGY.value

        # Return layer with highest average engagement
        best_layer = max(
            layer_scores,
            key=lambda l: sum(layer_scores[l]) / len(layer_scores[l])
        )
        return best_layer

    # -------------------------------------------------------------------------
    # Q3: Humor Mechanism Precedent (Boredom Ban)
    # -------------------------------------------------------------------------

    def _q3_humor_mechanism_precedent(
        self,
        humor_registry: HumorMechanismRegistry,
        lookback_weeks: int = 8,
    ) -> Optional[str]:
        """Q3: Is there a humor mechanism that should be rotated in for freshness?

        Spec: 'Boredom Ban enforcement — no mechanism repeated in last 8 weeks.'

        Returns the mechanism name of one that has NOT been used in the last
        lookback_weeks weeks, if any.

        Args:
            humor_registry: The coach's humor mechanism registry.
            lookback_weeks: Look-back window for Boredom Ban (default 8).

        Returns:
            A mechanism name that is ready to use, or None if no registry data.
        """
        recent_names = set(humor_registry.get_recent_mechanisms(weeks=lookback_weeks))

        # Find mechanisms in the registry NOT used recently
        all_mechanisms = {entry.mechanism_name for entry in humor_registry.entries}
        available = all_mechanisms - recent_names

        if available:
            # Return first available (alphabetical for determinism)
            return sorted(available)[0]

        # All mechanisms used recently — nothing to enforce; return None
        return None

    # -------------------------------------------------------------------------
    # Main execution
    # -------------------------------------------------------------------------

    def run(
        self,
        session_cral_phase: str,
        story_archive: CoachStoryArchive,
        cmm: CulturalMemoryMap,
        performance_registry: ContextPerformanceRegistry,
        humor_registry: HumorMechanismRegistry,
        trigger_category: str = "",
        arc_phase: str = "",
    ) -> ContextSelectionObject:
        """Execute all 3 context reasoning questions and return ContextSelectionObject.

        Spec (DEP-ENG-025):
        - Q1: Story archive eligibility (M4 RESONANT check — AC5)
        - Q2: CMM layer performance weighting
        - Q3: Humor mechanism precedent (Boredom Ban)

        The ContextSelectionObject is the authoritative pre-compilation output
        consumed by the script generation pipeline.

        Args:
            session_cral_phase: CRAL phase for this session (e.g. 'M4_RESONANT').
            story_archive: Coach's confirmed story archive (DEP-ENG-024).
            cmm: Coach's confirmed cultural memory map (DEP-ENG-023).
            performance_registry: Context performance registry (DEP-ENG-045).
            humor_registry: Humor mechanism registry.
            trigger_category: The trigger category for this session (e.g. 'Worth').
            arc_phase: The arc phase targeted this session (e.g. 'breakthrough').

        Returns:
            ContextSelectionObject with all 3 Q answers populated.
        """
        # Q1 — Story archive
        story_used, story_id = self._q1_story_archive_check(story_archive, session_cral_phase)

        # Q2 — CMM layer
        cmm_layer = self._q2_cmm_layer_weighting(cmm, performance_registry)

        # Q3 — Humor mechanism
        humor_mechanism = self._q3_humor_mechanism_precedent(humor_registry)

        cso = ContextSelectionObject(
            session_id=f"SESSION-{self.coach_acronym}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            coach_id=self.coach_id,
            trigger_category=trigger_category or session_cral_phase,
            arc_phase=arc_phase or session_cral_phase,
            story_archive_used=story_used,
            story_id_selected=story_id,
            cmm_layer_selected=cmm_layer,
            humor_mechanism_selected=humor_mechanism,
        )

        # Persist CSO to local config for audit trail
        cso_path = self.coach_dir / "config" / f"context_selection_{cso.session_id}.json"
        cso_path.parent.mkdir(parents=True, exist_ok=True)
        cso_path.write_text(cso.model_dump_json(indent=2), encoding="utf-8")

        return cso

    def update_performance_registry(
        self,
        performance_registry: ContextPerformanceRegistry,
        cso: ContextSelectionObject,
        engagement_score: float,
        conversion_rate: float,
        content_ids: Optional[list[str]] = None,
    ) -> ContextPerformanceRegistry:
        """Update the context performance registry after a session completes.

        Called after engagement data is received to record what worked.
        Used by Q2 (CMM layer weighting) in subsequent sessions.

        Spec DEP-ENG-045: 'should_upgrade_confidence_model() at ≥5 sessions'

        Args:
            performance_registry: The current registry to update.
            cso: The ContextSelectionObject used in this session.
            engagement_score: Normalized engagement score 0.0–1.0.
            conversion_rate: Conversion rate for this session's content.
            content_ids: List of content IDs generated in this session.

        Returns:
            Updated ContextPerformanceRegistry.
        """
        session_record = {
            "session_id": cso.session_id,
            "arc_phase": cso.arc_phase,
            "trigger_category": cso.trigger_category,
            "cmm_layer_used": cso.cmm_layer_selected,
            "story_archive_used": cso.story_archive_used,
            "story_id": cso.story_id_selected,
            "humor_mechanism": cso.humor_mechanism_selected,
            "engagement_score": engagement_score,
            "conversion_rate": conversion_rate,
            "content_ids": content_ids or [],
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }

        performance_registry.session_history.append(session_record)
        performance_registry.total_sessions = len(performance_registry.session_history)

        # Check confidence model upgrade threshold (DEP-ENG-045: ≥5 sessions)
        if performance_registry.should_upgrade_confidence_model():
            performance_registry.confidence_model = "adaptive_routing_model"

        performance_registry.updated_at = datetime.now(timezone.utc)

        # Persist
        cpr_path = self.coach_dir / "config" / "context_performance_registry.json"
        cpr_path.write_text(performance_registry.model_dump_json(indent=2), encoding="utf-8")

        return performance_registry

    def load_performance_registry(self) -> Optional[ContextPerformanceRegistry]:
        """Load context performance registry from local config."""
        cpr_path = self.coach_dir / "config" / "context_performance_registry.json"
        if not cpr_path.exists():
            return None
        data = json.loads(cpr_path.read_text(encoding="utf-8"))
        return ContextPerformanceRegistry.model_validate(data)
