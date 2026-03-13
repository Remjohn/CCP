"""
CCP Azaria Memory Promoter
Task 5.03 — Evaluates episodic patterns for long-term memory promotion.

Scans client interaction patterns and proposes promotions:
- Episodic → Semantic (a pattern becomes a known truth about the client)
- Pattern → Insight (a recurring behavior becomes an actionable insight)

Operator reviews and approves/rejects/defers each promotion.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from src.ccp.core.receipt_chain import ReceiptChain


class PromotionCandidate(BaseModel):
    """A pattern flagged for promotion to long-term memory."""

    candidate_id: str
    person_id: str
    pattern_description: str
    evidence: list[str] = Field(default_factory=list)
    frequency: int = Field(description="Times this pattern appeared")
    consistency: float = Field(ge=0.0, le=1.0, description="How consistent across interactions")
    impact_score: float = Field(ge=0.0, le=1.0, description="Estimated coaching impact")
    confidence: float = Field(ge=0.0, le=1.0)
    promotion_type: str = Field(description="episodic_to_semantic or pattern_to_insight")
    proposed_memory: str = Field(description="What the promoted memory would say")
    status: str = Field(default="pending")  # pending, approved, rejected, deferred
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AzariaMemoryPromoter:
    """Evaluate and promote patterns to long-term memory."""

    MIN_FREQUENCY = 3  # Pattern must appear at least 3 times
    MIN_CONFIDENCE = 0.7  # Minimum confidence for promotion

    def __init__(self, coach_acronym: str):
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym)
        self._memory_dir = Path(
            f"coaches/{self.coach_acronym}/intelligence/memory"
        )
        self._promotions_file = self._memory_dir / "promotion_queue.jsonl"
        self._semantic_file = self._memory_dir / "semantic" / "promoted_memories.json"
        self._memory_dir.mkdir(parents=True, exist_ok=True)
        (self._memory_dir / "semantic").mkdir(parents=True, exist_ok=True)

    async def scan_for_promotions(self, person_id: str) -> list[PromotionCandidate]:
        """Scan a client's episodic memory for promotion candidates.

        Args:
            person_id: Client Person ID

        Returns:
            List of promotion candidates
        """
        from google import genai

        # Load episodic interactions
        interactions = self._load_episodes(person_id)
        if len(interactions) < self.MIN_FREQUENCY:
            return []

        # Use Gemini to detect patterns
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        interaction_text = "\n".join(
            f"[{i.get('type', '')}] {i.get('client_message', '')[:150]}"
            for i in interactions[-30:]  # Last 30 interactions
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""Analyze these coaching interactions for recurring patterns worth promoting to long-term memory.

INTERACTIONS:
{interaction_text}

Find patterns that:
1. Appear 3+ times across different conversations
2. Reveal something fundamental about this person's psychology
3. Would be valuable for a coach to remember long-term

Return JSON array:
[
  {{
    "pattern": "description of the recurring pattern",
    "evidence": ["quote 1", "quote 2", "quote 3"],
    "frequency": N,
    "consistency": 0.0-1.0,
    "impact_score": 0.0-1.0,
    "confidence": 0.0-1.0,
    "promotion_type": "episodic_to_semantic or pattern_to_insight",
    "proposed_memory": "The distilled memory statement"
  }}
]""",
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        try:
            raw_patterns = json.loads(text)
        except json.JSONDecodeError:
            return []

        candidates = []
        for i, raw in enumerate(raw_patterns):
            if raw.get("confidence", 0) < self.MIN_CONFIDENCE:
                continue
            if raw.get("frequency", 0) < self.MIN_FREQUENCY:
                continue

            import hashlib
            cid = hashlib.md5(
                f"{person_id}:{raw.get('pattern', '')}".encode()
            ).hexdigest()[:12]

            candidate = PromotionCandidate(
                candidate_id=cid,
                person_id=person_id,
                pattern_description=raw.get("pattern", ""),
                evidence=raw.get("evidence", []),
                frequency=raw.get("frequency", 0),
                consistency=raw.get("consistency", 0.5),
                impact_score=raw.get("impact_score", 0.5),
                confidence=raw.get("confidence", 0.7),
                promotion_type=raw.get("promotion_type", "episodic_to_semantic"),
                proposed_memory=raw.get("proposed_memory", ""),
            )
            candidates.append(candidate)

            # Save to queue
            with open(self._promotions_file, "a", encoding="utf-8") as f:
                f.write(candidate.model_dump_json() + "\n")

        self.receipt_chain.log(
            agent_id="azaria",
            action="scan_promotions",
            person_id=person_id,
            output_summary=f"Found {len(candidates)} promotion candidates",
            decision="completed",
            metadata={"candidate_count": len(candidates)},
        )

        return candidates

    def get_pending(self) -> list[PromotionCandidate]:
        """Get all pending promotion candidates."""
        if not self._promotions_file.exists():
            return []
        candidates = []
        with open(self._promotions_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    c = PromotionCandidate.model_validate_json(line)
                    if c.status == "pending":
                        candidates.append(c)
        return candidates

    def approve(self, candidate_id: str) -> None:
        """Approve a promotion — move to semantic memory."""
        candidate = self._update_status(candidate_id, "approved")
        if candidate:
            # Add to semantic memory
            memories = []
            if self._semantic_file.exists():
                memories = json.loads(self._semantic_file.read_text(encoding="utf-8"))
            memories.append({
                "person_id": candidate.person_id,
                "memory": candidate.proposed_memory,
                "evidence_count": len(candidate.evidence),
                "confidence": candidate.confidence,
                "promoted_at": datetime.now(timezone.utc).isoformat(),
            })
            self._semantic_file.write_text(json.dumps(memories, indent=2), encoding="utf-8")

            self.receipt_chain.log(
                agent_id="azaria",
                action="promote_memory",
                person_id=candidate.person_id,
                output_summary=f"Promoted: {candidate.proposed_memory[:80]}",
                decision="approved",
            )

    def reject(self, candidate_id: str) -> None:
        """Reject a promotion."""
        self._update_status(candidate_id, "rejected")

    def defer(self, candidate_id: str) -> None:
        """Defer a promotion for later review."""
        self._update_status(candidate_id, "deferred")

    def _update_status(self, candidate_id: str, new_status: str) -> Optional[PromotionCandidate]:
        if not self._promotions_file.exists():
            return None
        lines = self._promotions_file.read_text(encoding="utf-8").splitlines()
        updated = []
        target = None
        for line in lines:
            if not line.strip():
                continue
            c = PromotionCandidate.model_validate_json(line)
            if c.candidate_id == candidate_id:
                c.status = new_status
                target = c
            updated.append(c.model_dump_json())
        self._promotions_file.write_text("\n".join(updated) + "\n", encoding="utf-8")
        return target

    def _load_episodes(self, person_id: str) -> list[dict]:
        """Load episodic interactions for a client."""
        # person_id format: CCC-NNNN, extract the client telegram ID
        client_id = person_id.split("-")[-1] if "-" in person_id else person_id
        episodes_file = self._memory_dir / "episodic" / f"interactions_{client_id}.jsonl"
        if not episodes_file.exists():
            return []
        interactions = []
        with open(episodes_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    interactions.append(json.loads(line))
        return interactions
