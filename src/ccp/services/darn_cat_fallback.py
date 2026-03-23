"""
CCP FR5 Trigger Map Builder — DARN-CAT Fallback (Unit 9)
AC8: Backward compatibility — DARN-CAT legacy path when trigger_map.json missing.

Spec reference: FR5 Tech Spec §AC8
  'When trigger_map.json does not exist, the system falls back to the
  legacy DARN-CAT classification from the CBCS Change Talk Vault.
  This ensures backward compatibility during the transition period
  where coaches have not yet completed the Trigger Map Builder.'

  The DARN-CAT taxonomy (Miller & Rollnick, 2013):
    D = Desire — "I want to..."
    A = Ability — "I can..."
    R = Reason — "I need to because..."
    N = Need — "I have to..."
    C = Commitment — "I will..."
    A = Activation — "I'm ready to..."
    T = Taking Steps — "I've already started..."

Research basis:
  Miller & Rollnick (2013) Motivational Interviewing —
    Change Talk as trigger identification proxy
"""

import json
from pathlib import Path
from typing import Any, Optional

from src.ccp.models.trigger_map_models import (
    MoralFoundationMapping,
    MoralFoundationType,
    NarrativeIdentityClassification,
    NarrativePositioning,
    NarrativeSequenceType,
    OriginClassification,
    AKBLevel,
    PTGAssessment,
    PTGStatus,
    ReconsolidationSensitivity,
    TriggerEntry,
    TriggerEvidencePassage,
    TriggerMap,
)


# DARN-CAT category keywords
DARN_CAT_KEYWORDS: dict[str, list[str]] = {
    "desire": [
        "i want", "i wish", "i'd like", "i hope", "my dream",
        "i desire", "i long for", "if only",
    ],
    "ability": [
        "i can", "i could", "i'm able", "i know how",
        "i have the skill", "i've done it before",
    ],
    "reason": [
        "because", "the reason is", "it matters because",
        "i need to because", "the thing is",
    ],
    "need": [
        "i need to", "i have to", "i must", "it's essential",
        "i've got to", "i should",
    ],
    "commitment": [
        "i will", "i'm going to", "i commit", "i promise",
        "i intend to", "i've decided",
    ],
    "activation": [
        "i'm ready", "i'm prepared", "let's do this",
        "it's time", "i'm starting", "i've had enough",
    ],
    "taking_steps": [
        "i've already", "i started", "i began",
        "i took the first step", "yesterday i",
        "last week i", "i'm currently",
    ],
}

# DARN-CAT to moral foundation heuristic mapping
DARN_CAT_FOUNDATION_MAP: dict[str, MoralFoundationType] = {
    "desire": MoralFoundationType.LIBERTY_OPPRESSION,
    "ability": MoralFoundationType.FAIRNESS_CHEATING,
    "reason": MoralFoundationType.FAIRNESS_CHEATING,
    "need": MoralFoundationType.CARE_HARM,
    "commitment": MoralFoundationType.LOYALTY_BETRAYAL,
    "activation": MoralFoundationType.LIBERTY_OPPRESSION,
    "taking_steps": MoralFoundationType.AUTHORITY_SUBVERSION,
}


class DARNCATFallback:
    """Backward compatibility service for when trigger_map.json doesn't exist.

    AC8: 'When trigger_map.json does not exist, the system falls back to
    DARN-CAT classification from the CBCS Change Talk Vault.'

    This service generates a minimal trigger map from Change Talk data
    using the Miller & Rollnick (2013) DARN-CAT taxonomy as a proxy
    for trigger identification. The resulting map has lower classification
    depth than the full FR5 pipeline but provides operational continuity.
    """

    def check_trigger_map_exists(self, coach_dir: Path) -> bool:
        """Check if a trigger_map.json exists for this coach.

        Args:
            coach_dir: Path to the coach's data directory.

        Returns:
            True if trigger_map.json exists and has at least 1 trigger.
        """
        trigger_map_path = coach_dir / "intelligence_library" / "trigger_map.json"
        if not trigger_map_path.exists():
            return False

        try:
            with open(trigger_map_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            triggers = data.get("triggers", [])
            # Filter out template entries
            real_triggers = [
                t for t in triggers if not t.get("_template", False)
            ]
            return len(real_triggers) > 0
        except (json.JSONDecodeError, OSError):
            return False

    def generate_fallback_map(
        self,
        change_talk_entries: list[dict[str, Any]],
        coach_id: str = "",
        session_id: str = "",
    ) -> TriggerMap:
        """Generate a minimal trigger map from DARN-CAT Change Talk entries.

        Args:
            change_talk_entries: List of Change Talk Vault entries.
                Each entry should have: 'text', 'darn_cat_category',
                'client_id', 'timestamp'.
            coach_id: Coach identifier.
            session_id: Pipeline session identifier.

        Returns:
            A minimal TriggerMap with DARN-CAT-derived triggers.
        """
        trigger_map = TriggerMap(
            schema_version="1.0-fallback",
            coach_id=coach_id,
            description=(
                "DARN-CAT fallback trigger map — generated from Change Talk Vault "
                "when full FR5 Trigger Map Builder has not been executed. "
                "Lower classification depth than production trigger map."
            ),
        )

        # Group Change Talk by DARN-CAT category
        category_entries: dict[str, list[dict[str, Any]]] = {}
        for entry in change_talk_entries:
            category = entry.get("darn_cat_category", "unknown")
            if category not in category_entries:
                category_entries[category] = []
            category_entries[category].append(entry)

        # Build triggers from dominant categories
        for idx, (category, entries) in enumerate(category_entries.items()):
            if len(entries) < 2:
                continue  # Skip categories with insufficient evidence

            trigger = self._build_fallback_trigger(
                category=category,
                entries=entries,
                trigger_idx=idx,
                session_id=session_id,
            )
            # DARN-CAT triggers go to candidate_triggers (not fully resolved)
            trigger_map.candidate_triggers.append(trigger)

        trigger_map.compute_status()
        trigger_map.compute_confidence()
        return trigger_map

    def _build_fallback_trigger(
        self,
        category: str,
        entries: list[dict[str, Any]],
        trigger_idx: int,
        session_id: str,
    ) -> TriggerEntry:
        """Build a single trigger from DARN-CAT entries."""
        # Collect evidence
        evidence = [
            TriggerEvidencePassage(
                passage_text=str(e.get("text", ""))[:300],
                source_session_id=session_id,
                label=f"DARN-CAT:{category}",
                confidence=0.4,  # lower confidence for fallback
            )
            for e in entries[:5]
        ]

        # Extract keywords from entries
        keywords: list[str] = []
        for kw_list in DARN_CAT_KEYWORDS.get(category, []):
            if any(kw_list in str(e.get("text", "")).lower() for e in entries):
                keywords.append(kw_list)

        # Map to moral foundation using heuristic
        foundation = DARN_CAT_FOUNDATION_MAP.get(
            category, MoralFoundationType.CARE_HARM
        )

        # Combined text for description
        combined = " | ".join(
            str(e.get("text", ""))[:100] for e in entries[:3]
        )

        return TriggerEntry(
            trigger_id=f"darn_{trigger_idx + 1:03d}",
            label=f"darn_cat_{category}",
            description=f"DARN-CAT fallback: {category} — {combined[:300]}",
            moral_foundation=MoralFoundationMapping(
                primary=foundation,
            ),
            originating_experience=OriginClassification(
                akb_level=AKBLevel.GENERAL_EVENT,
                narrative_summary=f"Derived from {len(entries)} Change Talk entries",
                evidence_passages=evidence[:2],
            ),
            ptg_status=PTGAssessment(
                status=PTGStatus.ACTIVE_PROCESSING,
                resolution_signal="DARN-CAT fallback — status indeterminate",
                evidence_passages=evidence[:1],
            ),
            narrative_identity=NarrativeIdentityClassification(
                sequence_type=NarrativeSequenceType.MIXED,
                positioning=NarrativePositioning.SURVIVOR_GUIDE,
                evidence_passages=evidence[:1],
            ),
            reconsolidation_sensitivity=ReconsolidationSensitivity(
                score=5,  # neutral score for fallback
                v1_cross_validated=False,
                evidence_passages=evidence[:1],
            ),
            activation_keywords=keywords,
            evidence_passages=evidence,
        )
