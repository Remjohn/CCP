"""
FR-CBCS-01 — Change Talk Vault
================================
DARN-CAT commitment language extraction from client CBCS messages,
archival, and vault quality-gate querying.

Spec ref: FR_CBCS_01_Change_Talk_Vault_Tech_Spec.md
"""

from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cbcs_models import (
    DARN_CAT_PATTERNS,
    VAULT_PASS_THRESHOLD,
    VAULT_PROVISIONAL_MIN,
    ChangeTalkArchiveRow,
    ChangeTalkError,
    DarnCatDimension,
    VaultGateVerdict,
    VaultQueryResult,
)


class ChangeTalkTagger:
    """Extracts DARN-CAT commitment phrases from raw client messages.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(ChangeTalkError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain
        # Precompile patterns
        self._compiled: dict[str, re.Pattern[str]] = {
            dim: re.compile(pattern, re.IGNORECASE)
            for dim, pattern in DARN_CAT_PATTERNS.items()
        }

    # ── Stage 1 + Stage 3: Scan & Tag ─────────────────────────────────

    def extract(
        self,
        client_id: str,
        coach_id: str,
        raw_text: str,
        coping_stage: int = 2,
        emotional_mode: str = "Processing",
    ) -> list[ChangeTalkArchiveRow]:
        """Extract DARN-CAT tagged entries from raw client message text.

        Parameters
        ----------
        client_id : str
            Unique client identifier.
        coach_id : str
            Coach boundary (ADR-01).
        raw_text : str
            Raw CBCS client message text.
        coping_stage : int
            Current coping position (1-5) from FR-CBCS-04.
        emotional_mode : str
            Current emotional mode from FR18 CRAL.

        Returns
        -------
        list[ChangeTalkArchiveRow]
            Zero or more tagged entries. Empty if text is empty or no matches.
        """
        if not raw_text or len(raw_text.strip()) == 0:
            return []

        sentences = self._split_sentences(raw_text)
        entries: list[ChangeTalkArchiveRow] = []

        for sentence in sentences:
            dimension = self._classify_sentence(sentence)
            if dimension is None:
                continue
            intensity = self._compute_intensity(sentence, dimension)
            entry = ChangeTalkArchiveRow(
                entry_id=str(uuid.uuid4()),
                client_id=client_id,
                coach_id=coach_id,
                statement_text=sentence.strip(),
                darn_cat_dimension=dimension,
                liwc_intensity_score=round(intensity, 4),
                coping_stage_at_time=max(1, min(5, coping_stage)),
                emotional_mode=emotional_mode,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            entries.append(entry)

        self._rc.log(
            agent_id="change-talk-tagger",
            action="change-talk-extract",
            person_id=client_id,
            input_summary=f"text_len={len(raw_text)}, sentences={len(sentences)}",
            output_summary=f"extracted={len(entries)} DARN-CAT entries",
        )
        return entries

    # ── Sentence Splitting ─────────────────────────────────────────────

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """Split text on terminal punctuation (.!?) preserving sentence text."""
        # Split on sentence-ending punctuation, keep non-empty parts
        parts = re.split(r'(?<=[.!?])\s+', text.strip())
        return [p.strip() for p in parts if p.strip()]

    # ── DARN-CAT Classification (§4 Stage 3 — priority order) ─────────

    def _classify_sentence(self, sentence: str) -> str | None:
        """Classify a single sentence into a DARN-CAT dimension.

        Priority order: Need → Commitment → Taking_Steps → Activation →
        Desire → Ability → Reasons.

        Need takes priority per AC1: "I must do this because I was promised
        a raise." → Need (not Commitment, not Reasons).
        """
        # Priority order ensures AC1 compliance
        priority_order = [
            DarnCatDimension.NEED.value,
            DarnCatDimension.COMMITMENT.value,
            DarnCatDimension.TAKING_STEPS.value,
            DarnCatDimension.ACTIVATION.value,
            DarnCatDimension.DESIRE.value,
            DarnCatDimension.ABILITY.value,
            DarnCatDimension.REASONS.value,
        ]
        for dim in priority_order:
            if self._compiled[dim].search(sentence):
                return dim
        return None

    # ── Intensity Score ────────────────────────────────────────────────

    def _compute_intensity(self, sentence: str, dimension: str) -> float:
        """Compute liwc_intensity_score: matched word frequency * 100.

        (matched_words / total_words) * 100 → float 0.0-100.0
        """
        words = sentence.split()
        total = len(words)
        if total == 0:
            return 0.0
        pattern = self._compiled.get(dimension)
        if pattern is None:
            return 0.0
        matched = sum(1 for w in words if pattern.search(w))
        return min(100.0, (matched / total) * 100.0)


class ChangeTalkVault:
    """In-memory vault for querying archived change-talk entries.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Immutable audit trail.
    """

    def __init__(self, coach_acronym: str, receipt_chain: ReceiptChain) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(ChangeTalkError.INVALID_COACH_SCOPE.value)
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ── Stage 5: Quality Gate & Retrieval ──────────────────────────────

    def query_vault(
        self,
        client_id: str,
        coach_id: str,
        archive: list[ChangeTalkArchiveRow],
    ) -> VaultQueryResult:
        """Evaluate Minimum Vault Threshold Gate for a client.

        Parameters
        ----------
        client_id : str
            Target client.
        coach_id : str
            Coach boundary (ADR-01).
        archive : list[ChangeTalkArchiveRow]
            All entries for this client in this coach scope.

        Returns
        -------
        VaultQueryResult
            Verdict + optional top statement.
        """
        # ADR-01: filter to exact coach scope
        scoped = [
            e for e in archive
            if e.client_id == client_id and e.coach_id == coach_id
        ]
        total = len(scoped)

        # Count Commitment + Taking_Steps entries
        commitment_dims = {
            DarnCatDimension.COMMITMENT.value,
            DarnCatDimension.TAKING_STEPS.value,
        }
        commitment_entries = [
            e for e in scoped if e.darn_cat_dimension in commitment_dims
        ]
        commitment_count = len(commitment_entries)

        # Gate evaluation (§4 Stage 5)
        if commitment_count >= VAULT_PASS_THRESHOLD:
            verdict = VaultGateVerdict.PASS.value
            confidence_flag = None
            top = max(commitment_entries, key=lambda e: e.liwc_intensity_score)
        elif commitment_count >= VAULT_PROVISIONAL_MIN:
            verdict = VaultGateVerdict.PROVISIONAL.value
            confidence_flag = "PROVISIONAL"
            top = max(commitment_entries, key=lambda e: e.liwc_intensity_score)
        else:
            verdict = VaultGateVerdict.FAIL.value
            confidence_flag = None
            top = None

        result = VaultQueryResult(
            client_id=client_id,
            coach_id=coach_id,
            total_entries=total,
            commitment_count=commitment_count,
            verdict=verdict,
            confidence_flag=confidence_flag,
            top_statement=top,
        )

        self._rc.log(
            agent_id="change-talk-vault",
            action="vault-query",
            person_id=client_id,
            input_summary=f"total_entries={total}, commitment_count={commitment_count}",
            output_summary=f"verdict={verdict}",
        )
        return result
