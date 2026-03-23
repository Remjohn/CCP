"""
FR-VIS-02 — TIAR Adapter
Phase 2B, CVE Visual Engine — spec 4 of 13

Dual-firing integration layer that queries the Tribal Imagen Activation
Registry (DEP-VIS-001) at two pipeline points:
1. Upstream — During Script Generation Skills, before hook text assembly.
2. Downstream — During Abel's VCB generation, before visual text finalization.

Spec Reference: FR-VIS-02_TIAR_Integration_Tech_Spec.md
Every function traces to an explicit spec section.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    DecayStage,
    NounAuditEntry,
    NounDecayAudit,
    SlideNounAudit,
    TIARAdapterError,
    TIARInjectionResult,
    TIARNounEntry,
    TIARValidationResult,
    TIRS_EXPIRED_MAX,
    TIRS_IN_DISTRIBUTION_MIN,
)


class TIARAdapter:
    """Tribal Imagen Activation Registry Adapter — FR-VIS-02.

    Per FR-VIS-02 §2: dual-firing integration layer that queries DEP-VIS-001
    at upstream (script generation) and downstream (VCB finalization) points.

    Pipeline position: DEP-VIS-001 → TIAR Adapter (this) → Script Gen / VCB
    """

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: Optional[ReceiptChain] = None,
        tiar_data: Optional[list[TIARNounEntry]] = None,
    ):
        """Initialize the TIAR adapter.

        Args:
            coach_acronym: ADR-01 coach scope identifier (2-4 chars).
            receipt_chain: Optional ReceiptChain for audit logging.
            tiar_data: Optional pre-loaded TIAR data (for testing).
                       In production, this would be fetched from Notion.
        """
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got {len(coach_acronym)}"
            )
        self.coach_acronym = coach_acronym.upper()
        self.receipt_chain = receipt_chain or ReceiptChain(
            coach_acronym=self.coach_acronym[:3]
        )

        # Raw TIAR data — in production, fetched from Notion via DEP-VIS-001
        self._tiar_data: list[TIARNounEntry] = tiar_data or []
        self._cache: Optional[list[TIARNounEntry]] = None
        self._cache_timestamp: Optional[str] = None
        self._initialized: bool = len(self._tiar_data) > 0

    # ─────────────────────────────────────────────────
    # RECEIPT CHAIN INTEGRATION
    # ─────────────────────────────────────────────────

    def _write_receipt(
        self,
        stage_name: str,
        content_output_id: str,
        input_summary: str,
        output_summary: str,
        decision: str,
        decision_rationale: str,
        parent_receipt_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Write a receipt per FR47 DEP-ENG-041."""
        entry = self.receipt_chain.log(
            agent_id="tiar_adapter",
            action=stage_name,
            asset_id=content_output_id,
            input_summary=input_summary,
            output_summary=output_summary,
            decision=decision,
            decision_rationale=decision_rationale,
            parent_receipt_id=parent_receipt_id,
            metadata=metadata or {},
        )
        return entry.receipt_id

    # ─────────────────────────────────────────────────
    # TIAR QUERY — FR-VIS-02 §4 Stage 1 Step 2-3
    # ─────────────────────────────────────────────────

    def query_tiar(
        self,
        simulate_timeout: bool = False,
    ) -> tuple[list[TIARNounEntry], str]:
        """Query the TIAR registry.

        In production, this would call the Notion API.
        In tests, uses pre-loaded tiar_data.

        Args:
            simulate_timeout: If True, simulates an API timeout for cache tests.

        Returns:
            Tuple of (noun entries, cache_status: 'FRESH' or 'TIAR_CACHE_STALE').
        """
        if simulate_timeout:
            if self._cache is not None:
                return self._cache, "TIAR_CACHE_STALE"
            return [], "TIAR_CACHE_STALE"

        # Fresh query (or pre-loaded data)
        result = list(self._tiar_data)
        self._cache = list(result)
        self._cache_timestamp = datetime.now(timezone.utc).isoformat()
        return result, "FRESH"

    def update_tiar_data(self, new_data: list[TIARNounEntry]) -> None:
        """Update the TIAR data (simulates mid-pipeline refresh).

        Used in tests to simulate noun decay between upstream and downstream.
        """
        self._tiar_data = list(new_data)
        self._initialized = len(new_data) > 0

    # ─────────────────────────────────────────────────
    # NOUN PARTITIONING — FR-VIS-02 §4 Stage 1 Step 4
    # ─────────────────────────────────────────────────

    @staticmethod
    def partition_nouns(
        nouns: list[TIARNounEntry],
    ) -> tuple[list[TIARNounEntry], list[TIARNounEntry]]:
        """Partition nouns into active vocabulary and blocked list.

        Per FR-VIS-02 §4 Stage 1 Step 4:
        - in_distribution (TIRS ≥ 7.0): active
        - tribal_potential (TIRS 5.0-6.9): active with is_emerging=True
        - decay_approaching (TIRS 5.0-6.9): active with decay_warning=True
        - expired (TIRS < 5.0): blocked

        Returns:
            Tuple of (active_noun_vocabulary, blocked_noun_list).
        """
        active: list[TIARNounEntry] = []
        blocked: list[TIARNounEntry] = []

        for noun in nouns:
            if noun.decay_stage == DecayStage.EXPIRED:
                blocked.append(noun)
            elif noun.decay_stage == DecayStage.IN_DISTRIBUTION:
                active.append(noun.model_copy(update={"is_emerging": False, "decay_warning": False}))
            elif noun.decay_stage == DecayStage.TRIBAL_POTENTIAL:
                active.append(noun.model_copy(update={"is_emerging": True, "decay_warning": False}))
            elif noun.decay_stage == DecayStage.DECAY_APPROACHING:
                active.append(noun.model_copy(update={"is_emerging": False, "decay_warning": True}))

        return active, blocked

    # ─────────────────────────────────────────────────
    # STAGE 1: UPSTREAM TIAR INJECTION
    # FR-VIS-02 §4 Stage 1
    # ─────────────────────────────────────────────────

    def inject_upstream(
        self,
        coach_id: str,
        content_output_id: str = "upstream",
        tribe_id: str = "default",
        simulate_timeout: bool = False,
    ) -> TIARInjectionResult:
        """Stage 1: Upstream TIAR injection for Script Generation Skills.

        Queries DEP-VIS-001, partitions nouns, returns active vocabulary
        and blocked list. Pipeline continues even on API timeout (uses cache).

        Args:
            coach_id: Coach identifier.
            content_output_id: Content output ID for traceability.
            tribe_id: Tribe identifier.
            simulate_timeout: Simulate Notion API timeout.

        Returns:
            TIARInjectionResult with active vocabulary and blocked list.
        """
        now = datetime.now(timezone.utc).isoformat()

        # §6 Fallback: TIAR not initialized
        if not self._initialized and not simulate_timeout:
            result = TIARInjectionResult(
                coach_id=coach_id,
                tribe_id=tribe_id,
                query_timestamp_utc=now,
                active_noun_vocabulary=[],
                blocked_noun_list=[],
                vocabulary_size_active=0,
                vocabulary_size_blocked=0,
                cache_status="TIAR_NOT_INITIALIZED",
            )
            self._write_receipt(
                stage_name="VIS02_UPSTREAM_INJECTION",
                content_output_id=content_output_id,
                input_summary=f"Coach {coach_id}, tribe {tribe_id}",
                output_summary="TIAR_NOT_INITIALIZED: empty vocabulary",
                decision="tiar_not_initialized",
                decision_rationale="TIAR registry has no data for this coach",
                metadata={"coach_id": coach_id, "tribe_id": tribe_id},
            )
            return result

        # Query TIAR
        nouns, cache_status = self.query_tiar(simulate_timeout=simulate_timeout)
        active, blocked = self.partition_nouns(nouns)

        result = TIARInjectionResult(
            coach_id=coach_id,
            tribe_id=tribe_id,
            query_timestamp_utc=now,
            active_noun_vocabulary=active,
            blocked_noun_list=blocked,
            vocabulary_size_active=len(active),
            vocabulary_size_blocked=len(blocked),
            cache_status=cache_status,
        )

        receipt_id = self._write_receipt(
            stage_name="VIS02_UPSTREAM_INJECTION",
            content_output_id=content_output_id,
            input_summary=(
                f"Coach {coach_id}, tribe {tribe_id}, "
                f"query returned {len(nouns)} nouns"
            ),
            output_summary=(
                f"Active: {len(active)}, Blocked: {len(blocked)}, "
                f"Cache: {cache_status}"
            ),
            decision="injection_complete",
            decision_rationale=(
                f"Partitioned {len(nouns)} nouns into "
                f"{len(active)} active + {len(blocked)} blocked"
            ),
            metadata={
                "coach_id": coach_id,
                "tribe_id": tribe_id,
                "active_count": len(active),
                "blocked_count": len(blocked),
                "cache_status": cache_status,
            },
        )

        result.receipt_chain_block = receipt_id
        return result

    # ─────────────────────────────────────────────────
    # TEXT CHECKING — FR-VIS-02 §4 Stage 1 Step 6
    # ─────────────────────────────────────────────────

    def check_text_for_blocked_nouns(
        self,
        text: str,
        injection_result: TIARInjectionResult,
    ) -> tuple[bool, list[str], list[TIARNounEntry]]:
        """Check if text contains any blocked (expired) nouns.

        Per FR-VIS-02 §4 Stage 1 Step 6: rejected for rewording.

        Args:
            text: Hook text or slide text to check.
            injection_result: Result from inject_upstream().

        Returns:
            Tuple of (text_ok, list of expired noun strings found,
            active replacements).
        """
        text_lower = text.lower()
        found_blocked: list[str] = []

        for noun_entry in injection_result.blocked_noun_list:
            if noun_entry.noun.lower() in text_lower:
                found_blocked.append(noun_entry.noun)

        if found_blocked:
            # Offer active replacements
            replacements = [
                n for n in injection_result.active_noun_vocabulary
                if n.decay_stage == DecayStage.IN_DISTRIBUTION
            ]
            return False, found_blocked, replacements

        return True, [], []

    # ─────────────────────────────────────────────────
    # NOUN EXTRACTION — FR-VIS-02 §4 Stage 2 Step 2
    # ─────────────────────────────────────────────────

    def extract_nouns_from_text(
        self,
        text: str,
        tiar_nouns: list[TIARNounEntry],
    ) -> tuple[list[NounAuditEntry], list[str]]:
        """Extract TIAR nouns from slide text.

        Per FR-VIS-02 §4 Stage 2 Steps 2-5: matches multi-word phrases.

        Args:
            text: The slide text to search.
            tiar_nouns: All TIAR nouns from the fresh query.

        Returns:
            Tuple of (found TIAR noun audit entries, nouns NOT in registry).
        """
        text_lower = text.lower()
        found: list[NounAuditEntry] = []
        matched_spans: list[tuple[int, int]] = []

        # Sort by length descending to match longest phrases first
        sorted_nouns = sorted(tiar_nouns, key=lambda n: len(n.noun), reverse=True)

        for noun_entry in sorted_nouns:
            noun_lower = noun_entry.noun.lower()
            pos = text_lower.find(noun_lower)
            if pos >= 0:
                # Check no overlap with already matched spans
                end = pos + len(noun_lower)
                overlaps = any(
                    not (end <= s or pos >= e) for s, e in matched_spans
                )
                if not overlaps:
                    matched_spans.append((pos, end))

                    if noun_entry.decay_stage == DecayStage.EXPIRED:
                        status = "NOUN_EXPIRED_SINCE_SCRIPT"
                    elif noun_entry.decay_stage == DecayStage.DECAY_APPROACHING:
                        status = "NOUN_DECAY_WARNING"
                    else:
                        status = "NOUN_ACTIVE"

                    found.append(NounAuditEntry(
                        noun=noun_entry.noun,
                        tirs_score=noun_entry.tirs_score,
                        decay_stage=noun_entry.decay_stage,
                        position_in_text=pos,
                        last_measured_date=noun_entry.last_measured_date,
                        status=status,
                    ))

        # Extract words not matched by TIAR — simplified: single words not in TIAR
        words_in_text = set(text_lower.split())
        tiar_words = set()
        for n in tiar_nouns:
            for w in n.noun.lower().split():
                tiar_words.add(w)
        not_in_registry = sorted(words_in_text - tiar_words - _STOP_WORDS)

        return found, not_in_registry

    # ─────────────────────────────────────────────────
    # STAGE 2: DOWNSTREAM TIAR RE-VALIDATION
    # FR-VIS-02 §4 Stage 2
    # ─────────────────────────────────────────────────

    def validate_downstream(
        self,
        content_output_id: str,
        slide_texts: list[Optional[str]],
        simulate_timeout: bool = False,
    ) -> TIARValidationResult:
        """Stage 2: Downstream TIAR re-validation for VCB finalization.

        Fires a fresh TIAR query and validates all text slides against it.
        Detects mid-pipeline decay transitions.

        Args:
            content_output_id: Content output ID for traceability.
            slide_texts: List of slide texts (None for image-only slides).
            simulate_timeout: Simulate Notion API timeout.

        Returns:
            TIARValidationResult with per-slide audit and any violations.
        """
        # §6 Fallback: TIAR not initialized
        if not self._initialized and not simulate_timeout:
            audit = NounDecayAudit(
                content_output_id=content_output_id,
                slide_audits=[
                    SlideNounAudit(slide_index=i)
                    for i in range(len(slide_texts))
                ],
            )
            result = TIARValidationResult(
                valid=True,
                noun_decay_audit=audit,
                tiar_status="TIAR_NOT_INITIALIZED",
                cache_status="TIAR_NOT_INITIALIZED",
                warnings=["TIAR_NOT_INITIALIZED: skipping noun validation for new coach"],
            )
            self._write_receipt(
                stage_name="VIS02_DOWNSTREAM_VALIDATION",
                content_output_id=content_output_id,
                input_summary=f"{len(slide_texts)} slides, TIAR not initialized",
                output_summary="TIAR_NOT_INITIALIZED: validation skipped",
                decision="tiar_not_initialized",
                decision_rationale="TIAR registry not populated for this coach",
            )
            return result

        # Fresh TIAR query
        nouns, cache_status = self.query_tiar(simulate_timeout=simulate_timeout)
        if simulate_timeout:
            cache_status = "TIAR_STALE_DOWNSTREAM"

        # Build per-slide audit
        slide_audits: list[SlideNounAudit] = []
        all_expired: list[str] = []
        total_tiar = 0
        total_active = 0
        total_decay_warning = 0
        total_expired = 0

        for idx, text in enumerate(slide_texts):
            if text is None or text.strip() == "":
                slide_audits.append(SlideNounAudit(slide_index=idx))
                continue

            found_entries, not_in_registry = self.extract_nouns_from_text(text, nouns)

            violations: list[str] = []
            warnings: list[str] = []

            for entry in found_entries:
                total_tiar += 1
                if entry.status == "NOUN_EXPIRED_SINCE_SCRIPT":
                    total_expired += 1
                    violations.append(
                        f"NOUN_EXPIRED_SINCE_SCRIPT: '{entry.noun}' "
                        f"(TIRS {entry.tirs_score}, stage: {entry.decay_stage})"
                    )
                    all_expired.append(entry.noun)
                elif entry.status == "NOUN_DECAY_WARNING":
                    total_decay_warning += 1
                    warnings.append(
                        f"NOUN_DECAY_WARNING: '{entry.noun}' is approaching decay "
                        f"(TIRS {entry.tirs_score}, stage: {entry.decay_stage})"
                    )
                else:
                    total_active += 1

            slide_audits.append(SlideNounAudit(
                slide_index=idx,
                nouns_found=found_entries,
                nouns_not_in_registry=not_in_registry,
                violations=violations,
                warnings=warnings,
            ))

        audit = NounDecayAudit(
            content_output_id=content_output_id,
            slide_audits=slide_audits,
            total_tiar_nouns=total_tiar,
            total_active=total_active,
            total_decay_warning=total_decay_warning,
            total_expired=total_expired,
        )

        # Determine validation result
        has_expired = total_expired > 0
        replacements: list[TIARNounEntry] = []
        if has_expired:
            active_pool, _ = self.partition_nouns(nouns)
            replacements = [
                n for n in active_pool
                if n.decay_stage == DecayStage.IN_DISTRIBUTION
            ]

        result = TIARValidationResult(
            valid=not has_expired,
            noun_decay_audit=audit,
            expired_nouns=all_expired,
            replacement_nouns=replacements,
            error_type=(
                TIARAdapterError.NOUN_EXPIRED_SINCE_SCRIPT.value
                if has_expired else None
            ),
            error_detail=(
                f"Expired nouns detected: {all_expired}"
                if has_expired else None
            ),
            tiar_status=(
                "TIAR_DECAY_DETECTED" if has_expired else "TIAR_VALID"
            ),
            cache_status=cache_status,
            warnings=[
                w for sa in slide_audits for w in sa.warnings
            ],
        )

        # Receipt write
        receipt_id = self._write_receipt(
            stage_name="VIS02_DOWNSTREAM_VALIDATION",
            content_output_id=content_output_id,
            input_summary=(
                f"{len(slide_texts)} slides, {len(nouns)} TIAR nouns queried"
            ),
            output_summary=(
                f"Valid: {result.valid}, Active: {total_active}, "
                f"Decay warnings: {total_decay_warning}, "
                f"Expired: {total_expired}, Cache: {cache_status}"
            ),
            decision="tiar_valid" if result.valid else "tiar_decay_detected",
            decision_rationale=(
                f"No expired nouns, {total_active} active nouns validated"
                if result.valid
                else f"Expired nouns: {all_expired}"
            ),
            metadata={
                "total_tiar_nouns": total_tiar,
                "total_active": total_active,
                "total_decay_warning": total_decay_warning,
                "total_expired": total_expired,
                "expired_nouns": all_expired,
                "cache_status": cache_status,
            },
        )

        if audit is not None:
            audit.receipt_chain_block = receipt_id

        return result

    # ─────────────────────────────────────────────────
    # STAGE 3: VPO AUDIT LOGGING
    # FR-VIS-02 §4 Stage 3
    # ─────────────────────────────────────────────────

    def log_vpo_audit(
        self,
        validation_result: TIARValidationResult,
    ) -> Optional[str]:
        """Stage 3: Log the noun decay audit to VPO record.

        Per FR-VIS-02 §4 Stage 3: non-blocking, audit failure does not halt pipeline.

        Returns:
            Receipt chain block ID, or None on failure.
        """
        audit = validation_result.noun_decay_audit
        if audit is None:
            return None

        try:
            receipt_id = self._write_receipt(
                stage_name="VIS02_VPO_AUDIT",
                content_output_id=audit.content_output_id,
                input_summary=(
                    f"Audit {audit.audit_id}: {audit.total_tiar_nouns} nouns, "
                    f"{len(audit.slide_audits)} slides"
                ),
                output_summary=(
                    f"Active: {audit.total_active}, "
                    f"Decay: {audit.total_decay_warning}, "
                    f"Expired: {audit.total_expired}"
                ),
                decision="vpo_audit_logged",
                decision_rationale="Noun decay audit attached to VPO record",
                metadata={
                    "audit_id": audit.audit_id,
                    "total_tiar_nouns": audit.total_tiar_nouns,
                },
            )
            return receipt_id
        except Exception:
            # §4 Stage 3: audit logging failure is non-blocking
            return None


# ─────────────────────────────────────────────────────
# STOP WORDS — filtered from "not_in_registry" lists
# ─────────────────────────────────────────────────────

_STOP_WORDS: frozenset[str] = frozenset({
    "a", "an", "the", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "shall",
    "can", "need", "dare", "ought", "used", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into",
    "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "not", "only", "own", "same",
    "so", "than", "too", "very", "just", "because", "but", "and",
    "or", "if", "while", "that", "this", "these", "those", "it",
    "its", "i", "me", "my", "we", "our", "you", "your", "he",
    "him", "his", "she", "her", "they", "them", "their", "what",
    "which", "who", "whom",
})
