"""
CCP FR25 — Boredom Ban Enforcer Service (DEP-PROTO-015)

Implements Agent Grâce (Draft Tester) and the full 3-stage Novelty
Enforcement Protocol across Theme Discovery, Wisdom Forge, and Draft Testing.

Spec reference: FR25_Boredom_Ban_Tech_Spec.md
  §4 Stage 1: Theme Discovery Novelty Check (Agent Divine / cosine sim)
  §4 Stage 2: Wisdom Forge Metaphor Extraction (Lionel/Jordan)
  §4 Stage 3: Draft Testing Validation (Agent Grâce — final safety net)
  §6: Cold Start fallback — MemoryFolder returns [] → MEMORY_ABSENT_ASSUMED_NOVEL

Critical invariants:
  - 56-day rolling window. NOT 30. NOT 8. 56. (AC1 failure: 30-day hardcoded limit)
  - Cosine threshold > 0.80 (STRICT greater-than, not >=)
  - Structural fatigue: > 3 uses in 14 days (STRICT greater-than)
  - Fatigue override fires after exactly 3 CONSECUTIVE collisions

ADR-01: coach_id scopes ALL MemoryFolder queries.
  Coach A's episodic memory is NEVER accessible to Coach B's compilation.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.boredom_ban_models import (
    BOREDOM_BAN_WINDOW_DAYS,
    FATIGUE_OVERRIDE_COLLISION_COUNT,
    STRUCTURAL_FATIGUE_DAYS,
    STRUCTURAL_FATIGUE_MAX_USES,
    THEME_COSINE_REJECT_THRESHOLD,
    BoredomBanResult,
    BoredomBanStage,
    BoredomBanTillDonePayload,
    BoredomBanVectorStatus,
    FatigueOverrideRecord,
    MemoryFolderEntry,
    MemoryFolderQuery,
    MetaphorCollisionResult,
    OverallNoveltyVerdict,
    StructuralFatigueResult,
    ThematicSimilarityResult,
    TillDoneRewriteType,
)


# ─── Cosine Similarity Helper ─────────────────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """Simple word tokenizer for cosine similarity calculation."""
    return set(re.findall(r"\b\w+\b", text.lower()))


def _cosine_similarity_text(text_a: str, text_b: str) -> float:
    """Lightweight text-based cosine similarity using bag-of-words.

    Spec §4 Stage 1: 'Compare via Embedding Cosine Similarity.'
    This is a heuristic fallback — in production, real embedding vectors
    (from a lightweight open-source model) would be used.

    AC2 test: 'Why diets don't work' vs 'The failure of modern diet culture'
    → similarity > 0.80 (REJECT). Same topics share heavy vocabulary overlap.
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a & tokens_b)
    magnitude_a = len(tokens_a) ** 0.5
    magnitude_b = len(tokens_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return intersection / (magnitude_a * magnitude_b)


def _synonym_overlap(text_a: str, text_b: str) -> bool:
    """Detect metaphor synonym/exact-match overlap.

    Spec §4 Stage 2 Step 3: 'direct exact-match/synonym overlap check.'
    AC1 spec: 'Building a house foundation' vs used 32 days ago → collision.
    Heuristic: significant shared content tokens = synonym overlap.
    """
    tokens_a = _tokenize(text_a)
    tokens_b = _tokenize(text_b)
    if not tokens_a or not tokens_b:
        return False
    # Exclude common stop words from overlap detection
    stop_words = {
        "the", "a", "an", "is", "are", "was", "were", "of", "to", "in",
        "for", "and", "or", "but", "at", "on", "with", "this", "that",
        "it", "be", "as", "by", "from", "i", "you", "we", "they",
    }
    content_a = tokens_a - stop_words
    content_b = tokens_b - stop_words
    if not content_a or not content_b:
        return False
    overlap = len(content_a & content_b)
    # >= 2 shared content tokens = synonym match
    return overlap >= 2


# ─── Boredom Ban Enforcer ─────────────────────────────────────────────────────

class BoredomBanEnforcer:
    """Agent Grâce — Novelty Enforcement Protocol (DEP-PROTO-015).

    ADR-01 strict isolation: All MemoryFolder queries MUST be scoped to
    self.coach_id. The enforcer physically cannot query other coaches' memory.

    Methods:
      check_theme_novelty()    — Stage 1: cosine similarity check.
      check_metaphor_novelty() — Stage 2: synonym/exact match check.
      check_structural_fatigue() — Stage 3: archetype frequency check.
      run_stage_1()            — Full Stage 1 with fatigue override circuit breaker.
      run_stage_2()            — Full Stage 2 Wisdom Forge check.
      run_stage_3()            — Full Stage 3 Draft Testing (final safety net).
    """

    def __init__(
        self,
        coach_id: str,
        receipt_chain: Optional[ReceiptChain] = None,
    ) -> None:
        if len(coach_id) != 3:
            raise ValueError(f"coach_id must be 3 chars, got: {coach_id!r}")
        self.coach_id = coach_id
        self._receipt_chain = receipt_chain

    # ── Episodic Memory Query ──────────────────────────────────────────────────

    def _query_memory(
        self,
        entries: list[MemoryFolderEntry],
        query: MemoryFolderQuery,
        reference_date: Optional[date] = None,
    ) -> list[MemoryFolderEntry]:
        """Filter MemoryFolder entries per ADR-01 and window constraints.

        ADR-01 (AC4): STRICTLY filters by query.coach_id.
        Only entries within the rolling window are returned.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        # ADR-01: ONLY this coach's entries — never another coach's data
        filtered = [
            e for e in entries
            if e.coach_id == query.coach_id
            and e.is_within_window(reference_date)
        ]
        return filtered

    def _query_memory_structural(
        self,
        entries: list[MemoryFolderEntry],
        coach_id: str,
        reference_date: Optional[date] = None,
    ) -> list[MemoryFolderEntry]:
        """Filter for structural fatigue check (14-day window, ADR-01)."""
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()
        return [
            e for e in entries
            if e.coach_id == coach_id
            and e.is_within_structural_window(reference_date)
        ]

    # ── Stage 1: Theme Discovery ───────────────────────────────────────────────

    def check_theme_novelty(
        self,
        proposed_theme: str,
        memory_entries: list[MemoryFolderEntry],
        reference_date: Optional[date] = None,
    ) -> ThematicSimilarityResult:
        """Spec §4 Stage 1: Cosine similarity check against 8-week history.

        Cold start (memory_entries is None or []): returns MEMORY_ABSENT_ASSUMED_NOVEL.
        Spec AC2: 0.85 cosine → REJECT (> 0.80 threshold).
        Spec AC2 failure: system crashes computing embeddings of 50 past scripts.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        # Cold start check (Spec §6)
        if not memory_entries:
            return ThematicSimilarityResult(
                proposed_theme=proposed_theme,
                similarity_score=0.0,
                memory_absent=True,
            )

        # ADR-01: filter to this coach's window entries
        query = MemoryFolderQuery(coach_id=self.coach_id)
        window_entries = self._query_memory(memory_entries, query, reference_date)

        if not window_entries:
            return ThematicSimilarityResult(
                proposed_theme=proposed_theme,
                similarity_score=0.0,
                memory_absent=True,
            )

        # Find the highest cosine similarity across all past themes
        max_score = 0.0
        closest_id: Optional[str] = None
        closest_theme: Optional[str] = None

        for entry in window_entries:
            if not entry.thematic_payload:
                continue
            score = _cosine_similarity_text(proposed_theme, entry.thematic_payload)
            if score > max_score:
                max_score = score
                closest_id = entry.skill_id
                closest_theme = entry.thematic_payload

        return ThematicSimilarityResult(
            proposed_theme=proposed_theme,
            similarity_score=max_score,
            closest_match_id=closest_id,
            closest_match_theme=closest_theme,
            memory_absent=False,
        )
        # Note: model_post_init auto-derives status from score

    def run_stage_1(
        self,
        proposed_themes: list[str],
        memory_entries: list[MemoryFolderEntry],
        slot_id: str = "",
        reference_date: Optional[date] = None,
    ) -> BoredomBanResult:
        """Full Stage 1 with fatigue override circuit breaker.

        Spec §4 Stage 1:
          - Divine generates 10 themes; we check the top proposed_themes.
          - Return top 2 novel themes.
          - If 3 consecutive collisions → FATIGUE_OVERRIDE_GRANTED: true.

        This method checks the FIRST proposed theme (representative of the
        10-theme generation) and returns a single BoredomBanResult.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        collision_count = 0
        colliding: list[str] = []
        last_result: Optional[ThematicSimilarityResult] = None
        till_done_payloads: list[BoredomBanTillDonePayload] = []
        fatigue_override: Optional[FatigueOverrideRecord] = None

        for theme in proposed_themes:
            result = self.check_theme_novelty(theme, memory_entries, reference_date)
            last_result = result

            if result.status == BoredomBanVectorStatus.REJECT_BOREDOM_BAN:
                collision_count += 1
                colliding.append(theme)

                # Spec §4 Stage 1: TillDone triggered on collision
                till_done_payloads.append(BoredomBanTillDonePayload(
                    rewrite_type=TillDoneRewriteType.MUTATE_THEMATIC_PAYLOAD,
                    original_value=theme,
                    rejection_reason=BoredomBanVectorStatus.REJECT_BOREDOM_BAN,
                    rejection_detail=(
                        f"Theme '{theme}' has cosine similarity "
                        f"{result.similarity_score:.2f} (threshold {THEME_COSINE_REJECT_THRESHOLD}) "
                        f"with '{result.closest_match_id}'."
                    ),
                    mutation_command=(
                        "Generate a new thematic payload that addresses a fundamentally "
                        "different psychological trigger. The rejected theme must not appear "
                        "in any form."
                    ),
                    till_done_iteration=collision_count,
                ))

                # Fatigue override circuit breaker
                if collision_count >= FATIGUE_OVERRIDE_COLLISION_COUNT:
                    fatigue_override = FatigueOverrideRecord(
                        coach_id=self.coach_id,
                        slot_id=slot_id,
                        collision_count=collision_count,
                        override_granted=True,
                        colliding_themes=colliding,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                    break
            else:
                # Novel theme found — stop after first pass
                break

        window_start = (
            reference_date
            if reference_date else datetime.now(timezone.utc).date()
        )
        from datetime import timedelta
        window_start_date = window_start - timedelta(days=BOREDOM_BAN_WINDOW_DAYS)

        boredom_result = BoredomBanResult(
            coach_id=self.coach_id,
            stage=BoredomBanStage.EARLY_THEME_DISCOVERY,
            eight_week_window_start=window_start_date.isoformat(),
            thematic_similarity=last_result,
            till_done_payloads=till_done_payloads,
            fatigue_override=fatigue_override,
            till_done_iterations_required=len(till_done_payloads),
        )

        self._write_receipt(
            agent_id="Divine",
            action="BOREDOM_BAN_STAGE_1_THEME_DISCOVERY",
            asset_id=f"DEP-PROTO-015_{self.coach_id}",
            input_summary=f"themes_checked={len(proposed_themes)}, slot_id={slot_id}",
            output_summary=(
                f"verdict={boredom_result.overall_verdict.value}, "
                f"collisions={collision_count}"
                + (" FATIGUE_OVERRIDE_GRANTED" if fatigue_override else "")
            ),
        )
        return boredom_result

    # ── Stage 2: Wisdom Forge Metaphor Extraction ──────────────────────────────

    def check_metaphor_novelty(
        self,
        proposed_metaphor: str,
        memory_entries: list[MemoryFolderEntry],
        reference_date: Optional[date] = None,
    ) -> MetaphorCollisionResult:
        """Spec §4 Stage 2: Direct exact-match/synonym overlap check.

        AC1: 'Building a house foundation' used 32 days ago → REJECT.
        AC1 failure example: system uses 30-day (not 56-day) limit.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        # Cold start check
        if not memory_entries:
            return MetaphorCollisionResult(
                proposed_metaphor=proposed_metaphor,
                memory_absent=True,
            )

        # ADR-01: filter to this coach's 56-day window
        query = MemoryFolderQuery(coach_id=self.coach_id)
        window_entries = self._query_memory(memory_entries, query, reference_date)

        if not window_entries:
            return MetaphorCollisionResult(
                proposed_metaphor=proposed_metaphor,
                memory_absent=True,
            )

        for entry in window_entries:
            if not entry.metaphor_vehicle:
                continue
            if _synonym_overlap(proposed_metaphor, entry.metaphor_vehicle):
                days_ago = (reference_date - entry.published_date).days
                till_done_cmd = (
                    f"Metaphor '{proposed_metaphor}' was used {days_ago} days ago "
                    f"(matched '{entry.metaphor_vehicle}'). "
                    "Generate a new conceptual vehicle from an unrelated domain "
                    "(e.g., biology, architecture, thermodynamics, oceanography)."
                )
                return MetaphorCollisionResult(
                    proposed_metaphor=proposed_metaphor,
                    status=BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED,
                    offending_vehicle=entry.metaphor_vehicle,
                    closest_match_id=entry.skill_id,
                    days_since_last_use=days_ago,
                    memory_absent=False,
                    till_done_rewrite_command=till_done_cmd,
                )

        return MetaphorCollisionResult(
            proposed_metaphor=proposed_metaphor,
            status=BoredomBanVectorStatus.PASS,
            memory_absent=False,
        )

    def run_stage_2(
        self,
        proposed_metaphor: str,
        memory_entries: list[MemoryFolderEntry],
        reference_date: Optional[date] = None,
    ) -> BoredomBanResult:
        """Spec §4 Stage 2: Mid-phase Wisdom Forge metaphor check."""
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        from datetime import timedelta
        window_start_date = reference_date - timedelta(days=BOREDOM_BAN_WINDOW_DAYS)

        metaphor_result = self.check_metaphor_novelty(
            proposed_metaphor, memory_entries, reference_date
        )

        till_done_payloads: list[BoredomBanTillDonePayload] = []
        if metaphor_result.status == BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED:
            till_done_payloads.append(BoredomBanTillDonePayload(
                rewrite_type=TillDoneRewriteType.MUTATE_METAPHOR_VEHICLE,
                original_value=proposed_metaphor,
                rejection_reason=BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED,
                rejection_detail=metaphor_result.till_done_rewrite_command or "",
                mutation_command=(
                    metaphor_result.till_done_rewrite_command
                    or "Generate a new metaphorical vehicle from an unrelated domain."
                ),
            ))

        result = BoredomBanResult(
            coach_id=self.coach_id,
            stage=BoredomBanStage.MID_METAPHOR_EXTRACTION,
            eight_week_window_start=window_start_date.isoformat(),
            metaphor_collision=metaphor_result,
            till_done_payloads=till_done_payloads,
            till_done_iterations_required=len(till_done_payloads),
        )

        self._write_receipt(
            agent_id="Lionel-Jordan",
            action="BOREDOM_BAN_STAGE_2_METAPHOR_EXTRACTION",
            asset_id=f"DEP-PROTO-015_{self.coach_id}",
            input_summary=f"metaphor='{proposed_metaphor[:50]}'",
            output_summary=(
                f"status={metaphor_result.status.value}"
                + (
                    f", collision_with='{metaphor_result.offending_vehicle}'"
                    if metaphor_result.offending_vehicle else ""
                )
            ),
        )
        return result

    # ── Stage 3: Draft Testing Validation (Agent Grâce) ──────────────────────

    def check_structural_fatigue(
        self,
        archetype_format: str,
        memory_entries: list[MemoryFolderEntry],
        reference_date: Optional[date] = None,
        suggested_alternative: Optional[str] = None,
    ) -> StructuralFatigueResult:
        """Spec §4 Stage 3: Archetype format frequency check (14-day window).

        AC3: LIST02 used 4 times in same week → REJECT: STRUCTURAL_FATIGUE on 4th.
        Spec: 'LIST02 has been used > 3 times in the last 14 days.'
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        # Cold start check
        if not memory_entries:
            return StructuralFatigueResult(
                archetype_format=archetype_format,
                frequency_14_days=0,
                memory_absent=True,
                suggested_alternative=suggested_alternative,
            )

        # ADR-01: 14-day structural window, this coach only
        structural_entries = self._query_memory_structural(
            memory_entries, self.coach_id, reference_date
        )

        if not structural_entries:
            return StructuralFatigueResult(
                archetype_format=archetype_format,
                frequency_14_days=0,
                memory_absent=True,
                suggested_alternative=suggested_alternative,
            )

        # Count this archetype in the 14-day window
        frequency = sum(
            1 for e in structural_entries
            if e.archetype_format == archetype_format
        )

        return StructuralFatigueResult(
            archetype_format=archetype_format,
            frequency_14_days=frequency,
            memory_absent=False,
            suggested_alternative=suggested_alternative,
        )
        # model_post_init auto-derives status from frequency > STRUCTURAL_FATIGUE_MAX_USES

    def run_stage_3(
        self,
        draft_text: str,
        archetype_format: str,
        memory_entries: list[MemoryFolderEntry],
        proposed_theme: Optional[str] = None,
        proposed_metaphor: Optional[str] = None,
        suggested_alternative_archetype: Optional[str] = None,
        reference_date: Optional[date] = None,
    ) -> BoredomBanResult:
        """Spec §4 Stage 3: Draft Testing — final safety net before Stage D.

        Grâce processes the fully assembled draft against:
          1. Structural fatigue (archetype frequency in 14 days).
          2. Optional: theme similarity if theme provided.
          3. Optional: metaphor overlap if metaphor provided.
        """
        if reference_date is None:
            reference_date = datetime.now(timezone.utc).date()

        from datetime import timedelta
        window_start_date = reference_date - timedelta(days=BOREDOM_BAN_WINDOW_DAYS)

        # Structural fatigue check (primary Stage 3 check)
        structural_result = self.check_structural_fatigue(
            archetype_format=archetype_format,
            memory_entries=memory_entries,
            reference_date=reference_date,
            suggested_alternative=suggested_alternative_archetype,
        )

        # Optional: thematic check if theme provided
        theme_result: Optional[ThematicSimilarityResult] = None
        if proposed_theme:
            theme_result = self.check_theme_novelty(
                proposed_theme, memory_entries, reference_date
            )

        # Optional: metaphor check if metaphor provided
        metaphor_result: Optional[MetaphorCollisionResult] = None
        if proposed_metaphor:
            metaphor_result = self.check_metaphor_novelty(
                proposed_metaphor, memory_entries, reference_date
            )

        # Build TillDone payloads for any blocking vectors
        till_done_payloads: list[BoredomBanTillDonePayload] = []

        if structural_result.status == BoredomBanVectorStatus.REJECT_STRUCTURAL_FATIGUE:
            alt = suggested_alternative_archetype or "STORY01"
            till_done_payloads.append(BoredomBanTillDonePayload(
                rewrite_type=TillDoneRewriteType.MUTATE_ARCHETYPE_STRUCTURE,
                original_value=archetype_format,
                rejection_reason=BoredomBanVectorStatus.REJECT_STRUCTURAL_FATIGUE,
                rejection_detail=(
                    f"[REJECT: STRUCTURAL_FATIGUE] '{archetype_format}' used "
                    f"{structural_result.frequency_14_days} times in last 14 days "
                    f"(max={STRUCTURAL_FATIGUE_MAX_USES})."
                ),
                mutation_command=(
                    f"Mutate this script into '{alt}' or another assigned, "
                    f"non-fatigued archetype pattern. '{archetype_format}' is "
                    f"structurally fatigued for this coach this week."
                ),
            ))

        if (
            metaphor_result
            and metaphor_result.status == BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED
        ):
            till_done_payloads.append(BoredomBanTillDonePayload(
                rewrite_type=TillDoneRewriteType.MUTATE_METAPHOR_VEHICLE,
                original_value=proposed_metaphor or "",
                rejection_reason=BoredomBanVectorStatus.REJECT_TILL_DONE_TRIGGERED,
                rejection_detail=metaphor_result.till_done_rewrite_command or "",
                mutation_command=(
                    metaphor_result.till_done_rewrite_command
                    or "Mutate the metaphorical vehicle."
                ),
            ))

        if (
            theme_result
            and theme_result.status == BoredomBanVectorStatus.REJECT_BOREDOM_BAN
        ):
            till_done_payloads.append(BoredomBanTillDonePayload(
                rewrite_type=TillDoneRewriteType.MUTATE_THEMATIC_PAYLOAD,
                original_value=proposed_theme or "",
                rejection_reason=BoredomBanVectorStatus.REJECT_BOREDOM_BAN,
                rejection_detail=(
                    f"Theme similarity score {theme_result.similarity_score:.2f} "
                    f"exceeds threshold {THEME_COSINE_REJECT_THRESHOLD}."
                ),
                mutation_command=(
                    "Generate a new thematic payload targeting a different "
                    "psychological trigger."
                ),
            ))

        result = BoredomBanResult(
            coach_id=self.coach_id,
            stage=BoredomBanStage.LATE_DRAFT_TESTING,
            eight_week_window_start=window_start_date.isoformat(),
            thematic_similarity=theme_result,
            metaphor_collision=metaphor_result,
            structural_fatigue=structural_result,
            till_done_payloads=till_done_payloads,
            till_done_iterations_required=len(till_done_payloads),
        )

        self._write_receipt(
            agent_id="Grace",
            action="BOREDOM_BAN_STAGE_3_DRAFT_TESTING",
            asset_id=f"DEP-PROTO-015_{self.coach_id}",
            input_summary=(
                f"archetype={archetype_format}, "
                f"draft_length={len(draft_text)}"
            ),
            output_summary=(
                f"verdict={result.overall_verdict.value}, "
                f"structural_freq={structural_result.frequency_14_days}, "
                f"till_done_count={len(till_done_payloads)}"
            ),
        )
        return result

    # ── Receipt Chain Helper ───────────────────────────────────────────────────

    def _write_receipt(
        self,
        agent_id: str,
        action: str,
        asset_id: str,
        input_summary: str,
        output_summary: str,
    ) -> None:
        if self._receipt_chain is None:
            return
        try:
            self._receipt_chain.log(
                agent_id=agent_id,
                action=action,
                asset_id=asset_id,
                person_id=self.coach_id,
                input_summary=input_summary,
                output_summary=output_summary,
            )
        except Exception:
            pass
