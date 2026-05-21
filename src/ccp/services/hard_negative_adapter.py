"""Hard Negative Adapter — DEP-SDA-024 / FR-ERA3-24 abstraction interface.
Temporary adapter that later consumes the full hard-negative corpus from FR-ERA3-24."""
from __future__ import annotations
from src.ccp.models.directional_integrity_models import (
    DirectionalIntegrityEvidence, HardNegativeCandidate, HardNegativeEvaluationReport,
    DirectionalIntegrityFallbackReason,
)
from uuid import uuid4

def _id(p: str) -> str: return f"{p}-{uuid4().hex[:8].upper()}"

KNOWN_HARD_NEGATIVES: list[dict] = [
    {"id": "HN-PRESTIGE-THEATER", "label": "prestige theater", "divergence": ["earned authority vs performance domination", "reflective proof vs vanity display"]},
    {"id": "HN-COERCIVE-URGENCY", "label": "coercive urgency", "divergence": ["invitational belonging vs scarcity pressure", "authentic deadline vs manufactured panic"]},
    {"id": "HN-FALSE-BELONGING", "label": "false belonging", "divergence": ["genuine community vs tribal capture", "shared mission vs exclusion-based identity"]},
    {"id": "HN-SHAME-REWARD", "label": "public-shame reward framing", "divergence": ["accountability vs humiliation", "progress visibility vs shame leverage"]},
    {"id": "HN-MYSTICAL-AUTHORITY", "label": "mystical authority inflation", "divergence": ["earned expertise vs unfalsifiable guru claims", "evidence-based vs revelation-based authority"]},
]

class HardNegativeAdapter:
    def __init__(self, available: bool = True) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def evaluate(self, *, candidate_text: str, representation_geometry_id: str) -> HardNegativeEvaluationReport:
        if not self._available:
            return HardNegativeEvaluationReport(
                report_id=_id("HNR"), top_matches=[], strongest_adjacency_score=0.0,
                blocked_by_hard_negative=False,
                fallback_reason=DirectionalIntegrityFallbackReason.MISSING_HARD_NEGATIVE_SERVICE,
            )
        candidates: list[HardNegativeCandidate] = []
        text_lower = candidate_text.lower() if candidate_text else ""
        for hn in KNOWN_HARD_NEGATIVES:
            adjacency = 0.0
            if hn["label"] in text_lower:
                adjacency = 0.65
            elif any(axis.split(" vs ")[1].lower() in text_lower for axis in hn["divergence"]):
                adjacency = 0.35
            if adjacency > 0.10:
                candidates.append(HardNegativeCandidate(
                    hard_negative_id=hn["id"], adjacency_score=adjacency,
                    divergence_axes=hn["divergence"], failure_reason=f"Candidate text adjacent to {hn['label']}",
                    evidence=[DirectionalIntegrityEvidence(
                        evidence_id=_id("EVD"), source_kind="hard_negative",
                        summary=f"Adjacency to {hn['label']}: {adjacency:.2f}",
                        cited_values={"hard_negative_id": hn["id"], "adjacency": adjacency},
                    )],
                ))
        candidates.sort(key=lambda c: c.adjacency_score, reverse=True)
        strongest = candidates[0].adjacency_score if candidates else 0.0
        return HardNegativeEvaluationReport(
            report_id=_id("HNR"), top_matches=candidates[:5],
            strongest_adjacency_score=strongest,
            blocked_by_hard_negative=strongest >= 0.40,
        )
