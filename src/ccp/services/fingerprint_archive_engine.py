"""
CCP FR23 — Fingerprint Archive Engine Service (DEP-ENG-020)

Implements the 4-stage Fingerprint Archive Engine:
  Stage 1: Skill ID string synthesis.
  Stage 2: Archive registration (dep_snapshot + maturity=draft).
  Stage 3: Output Linkage API (Telemetry Listener).
  Stage 4: Promotion Tier Protocol (DEP-PROTO-012).

Spec reference: FR23_Skill_Fingerprint_ID_Tech_Spec.md
  §4 Stage 1: ID synthesis — SKILL-{ARCH}-{COACH}-{MOOD}-{REG}-{COHORT}-{DATE}-{SEQ}
  §4 Stage 2: Archive registration with dep_snapshot SHA-256 hashes.
  §4 Stage 3: Telemetry Listener — UNLINKED_ORPHAN_OUTPUT on missing skill_id.
  §4 Stage 4: DEP-PROTO-012 promotion logic (Draft→Tested→Stable→Reference).

ADR-01 (AC4): All archive writes are partitioned by coach_id.
  Emilio's payload MUST ONLY write to Emilio's archive bucket.
  Cross-tenant writes are a hard architectural violation.
"""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.fingerprint_archive_models import (
    STABLE_MINIMUM_OUTPUTS,
    STABLE_SAVE_MULTIPLIER,
    TESTED_MINIMUM_OUTPUTS,
    ArchiveRegistrationResult,
    ArchiveWriteError,
    AudienceCohort,
    DependencySnapshot,
    FingerprintArchiveRecord,
    MoodCode,
    OutputTelemetryPayload,
    PromotionEvaluationResult,
    RegulatoryFrame,
    SkillIDComponents,
    SkillMaturity,
    TelemetryListenerResponse,
)


# ─── Exceptions ───────────────────────────────────────────────────────────────

class ArchiveIntegrityError(RuntimeError):
    """Raised when a write would violate ADR-01 tenant isolation."""
    pass


class SkillIDNotFoundError(KeyError):
    """Raised when the Telemetry Listener cannot find the target skill_id."""
    pass


# ─── Cryptography Helper ──────────────────────────────────────────────────────

def _sha256_of_object(obj: object) -> str:
    """Deterministic SHA-256 of a serialisable object.

    Spec §4 Stage 2 Step 1:
    AC2: 'Running the same hashing algorithm on the coach's Voice DNA file
    from that exact timestamp produces the exact same hash.'
    Empty buffer / None → returns empty string (triggers AC2 failure detection).
    """
    if obj is None:
        return ""
    try:
        serialized = json.dumps(obj, default=str, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    except (TypeError, ValueError):
        return ""


def _sha256_of_string(value: str) -> str:
    """Spec §4 Stage 2: Deterministic hash of a JSON string."""
    if not value or not value.strip():
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


# ─── Fingerprint Archive Engine ───────────────────────────────────────────────

class FingerprintArchiveEngine:
    """Implements DEP-ENG-020 — Skill Fingerprint Archive Engine.

    In-memory archive store (dict partitioned by coach_id).
    In production this would be backed by fingerprint_archive.json per tenant.

    ADR-01 strict isolation: all operations validate coach_id matches the
    target record's coach_id before any mutation.
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
        # In-memory archive: {coach_id: {skill_id: FingerprintArchiveRecord}}
        self._archive: dict[str, dict[str, FingerprintArchiveRecord]] = {}

    # ── Stage 1: Fingerprint String Synthesis ─────────────────────────────────

    def synthesize_skill_id(
        self,
        arch_id: str,
        mood: MoodCode,
        regulatory_frame: RegulatoryFrame,
        cohort: AudienceCohort,
        compilation_date: Optional[date] = None,
    ) -> str:
        """Spec §4 Stage 1: Build the human-readable Skill ID.

        Spec §4 Stage 1 Step 3: Queries existing archive for same-day
        compilations to assign the sequence number starting at 001.

        AC1: Null pointers must not break the hyphenated format.
        E.g., 'SKILL-LIST02-ANA-E-PRO-N-20260315-001'
        """
        if compilation_date is None:
            compilation_date = datetime.now(timezone.utc).date()

        # Spec §4 Stage 1 Step 3: find same-day sequence count
        sequence = self._next_sequence_for_date(compilation_date)

        components = SkillIDComponents(
            arch_id=arch_id,
            coach_id=self.coach_id,
            mood=mood,
            regulatory_frame=regulatory_frame,
            cohort=cohort,
            compilation_date=compilation_date,
            sequence_number=sequence,
        )

        skill_id = components.synthesize()

        self._write_receipt(
            agent_id="ID-Synthesis-Engine",
            action="FINGERPRINT_STAGE_1_ID_SYNTHESIS",
            asset_id=f"DEP-ENG-020_{self.coach_id}",
            input_summary=(
                f"arch_id={arch_id}, mood={mood.value}, "
                f"frame={regulatory_frame.value}, cohort={cohort.value}, "
                f"date={compilation_date}"
            ),
            output_summary=f"skill_id={skill_id}",
        )
        return skill_id

    # ── Stage 2: Archive Registration ─────────────────────────────────────────

    def register_skill(
        self,
        skill_id: str,
        assembly_status: str,
        dep_eng_003_obj: Optional[object] = None,
        dep_eng_006_obj: Optional[object] = None,
        dep_eng_016_obj: Optional[object] = None,
        archetype_template_id: str = "",
        archetype_template_version: str = "",
        context: Optional[dict] = None,
    ) -> ArchiveRegistrationResult:
        """Spec §4 Stage 2: Register a new skill in DEP-ENG-020.

        Step 1: Generate SHA-256 hashes for DEP-ENG-003/006/016.
        Step 2: Construct JSON schema block.
        Step 3: Append to archive.
        Step 4: Save SKILL.md (mocked — file path returned in production).

        On success: dep_snapshot populated, outputs=[], maturity=draft.
        """
        dep_snapshot = DependencySnapshot(
            dep_eng_003=_sha256_of_object(dep_eng_003_obj),
            dep_eng_006=_sha256_of_object(dep_eng_006_obj),
            dep_eng_016=_sha256_of_object(dep_eng_016_obj),
        )

        record = FingerprintArchiveRecord(
            skill_id=skill_id,
            coach_id=self.coach_id,
            archetype_template_id=archetype_template_id,
            archetype_template_version=archetype_template_version,
            compilation_date=datetime.now(timezone.utc).date().isoformat(),
            maturity=SkillMaturity.DRAFT,
            assembly_status=assembly_status,
            context=context or {},
            dep_snapshot=dep_snapshot,
            outputs=[],
        )

        # Write to in-memory archive (ADR-01: partitioned by coach_id)
        if self.coach_id not in self._archive:
            self._archive[self.coach_id] = {}
        self._archive[self.coach_id][skill_id] = record

        receipt_hash = _sha256_of_string(record.model_dump_json())
        self._write_receipt(
            agent_id="Fingerprint-Archive-Engine",
            action="FINGERPRINT_STAGE_2_REGISTRATION",
            asset_id=f"DEP-ENG-020_{self.coach_id}_{skill_id}",
            input_summary=f"assembly_status={assembly_status}",
            output_summary=(
                f"registered skill_id={skill_id}, "
                f"dep_snapshot_populated={dep_snapshot.is_populated()}"
            ),
        )

        return ArchiveRegistrationResult(
            success=True,
            skill_id=skill_id,
            coach_id=self.coach_id,
            maturity=SkillMaturity.DRAFT,
            dep_snapshot_populated=dep_snapshot.is_populated(),
            receipt_hash=receipt_hash,
        )

    # ── Stage 3: Telemetry Listener (Output Linkage API) ──────────────────────

    def receive_telemetry(
        self,
        payload: OutputTelemetryPayload,
    ) -> TelemetryListenerResponse:
        """Spec §4 Stage 3: Listener receives engagement analytics payload.

        ADR-01 (AC4): Validates payload.coach_id == self.coach_id.
          Cross-tenant write → ArchiveIntegrityError (hard block).

        Spec §6 Backward Compatibility: skill_id absent from archive →
          UNLINKED_ORPHAN_OUTPUT warning. Does NOT destroy analytics data.
          Returns accepted=False with error code.

        After successful append → triggers Stage 4 promotion check.
        """
        # ADR-01 strict isolation check
        if payload.coach_id != self.coach_id:
            raise ArchiveIntegrityError(
                f"ADR-01 VIOLATION: payload.coach_id={payload.coach_id!r} "
                f"attempted write to coach={self.coach_id!r} archive. "
                f"Cross-tenant writes are prohibited."
            )

        # Find the target skill record
        coach_bucket = self._archive.get(self.coach_id, {})
        record = coach_bucket.get(payload.skill_id)

        if record is None:
            # UNLINKED_ORPHAN_OUTPUT: safe ignore per spec §6
            receipt_hash = _sha256_of_string(payload.model_dump_json())
            self._write_receipt(
                agent_id="Archive-Telemetry-Listener",
                action="FINGERPRINT_STAGE_3_ORPHAN_OUTPUT",
                asset_id=f"DEP-ENG-020_{self.coach_id}",
                input_summary=f"output_id={payload.output_id}, skill_id={payload.skill_id}",
                output_summary="UNLINKED_ORPHAN_OUTPUT — write safely ignored",
            )
            return TelemetryListenerResponse(
                accepted=False,
                skill_id=payload.skill_id,
                output_id=payload.output_id,
                error=ArchiveWriteError.UNLINKED_ORPHAN_OUTPUT,
                receipt_hash=receipt_hash,
            )

        # Append to outputs array
        record.outputs.append(payload)

        # Stage 4: Run promotion check
        promotion_result = self._run_promotion_check(record)

        receipt_hash = _sha256_of_string(payload.model_dump_json())
        self._write_receipt(
            agent_id="Archive-Telemetry-Listener",
            action="FINGERPRINT_STAGE_3_TELEMETRY_RECEIVED",
            asset_id=f"DEP-ENG-020_{self.coach_id}_{payload.skill_id}",
            input_summary=(
                f"output_id={payload.output_id}, "
                f"saves={payload.performance.saves}"
            ),
            output_summary=(
                f"appended to outputs (total={len(record.outputs)}), "
                f"promotion={promotion_result.new_maturity.value if promotion_result else 'none'}"
            ),
        )

        return TelemetryListenerResponse(
            accepted=True,
            skill_id=payload.skill_id,
            output_id=payload.output_id,
            promotion_result=promotion_result,
            receipt_hash=receipt_hash,
        )

    # ── Stage 4: Promotion Monitor (DEP-PROTO-012) ────────────────────────────

    def _run_promotion_check(
        self,
        record: FingerprintArchiveRecord,
        category_average_saves: float = 0.0,
    ) -> Optional[PromotionEvaluationResult]:
        """Spec §4 Stage 4: DEP-PROTO-012 promotion logic.

        Runs asynchronously (synchronously here) after Telemetry Listener appends.
        AC3: 'asynchronous monitor immediately changes maturity to Tested'
             after 3rd successful output.

        AC3 violation guard: assembly_failure==true outputs MUST NOT count.
        """
        previous_maturity = record.maturity
        new_maturity = record.evaluate_maturity(
            category_average_saves=category_average_saves,
        )

        # Update record in-place
        record.maturity = new_maturity
        if new_maturity == SkillMaturity.STABLE:
            record.promoted_to_stable = True
        if new_maturity == SkillMaturity.REFERENCE:
            record.promoted_to_reference = True

        result = PromotionEvaluationResult(
            skill_id=record.skill_id,
            coach_id=record.coach_id,
            previous_maturity=previous_maturity,
            new_maturity=new_maturity,
            promoted=(new_maturity != previous_maturity),
            successful_output_count=record.successful_output_count(),
            average_saves=record.average_saves(),
            category_average_saves=category_average_saves,
        )

        if result.promoted:
            receipt_hash = _sha256_of_string(result.model_dump_json())
            result.receipt_hash = receipt_hash
            self._write_receipt(
                agent_id="Archive-Promotion-Monitor",
                action="FINGERPRINT_STAGE_4_PROMOTION",
                asset_id=f"DEP-ENG-020_{self.coach_id}_{record.skill_id}",
                input_summary=(
                    f"previous={previous_maturity.value}, "
                    f"successful_outputs={result.successful_output_count}"
                ),
                output_summary=f"PROMOTED → {new_maturity.value}",
            )

        return result

    # ── Query Helpers ──────────────────────────────────────────────────────────

    def get_record(self, skill_id: str) -> Optional[FingerprintArchiveRecord]:
        """Retrieve a record by skill_id (coach-scoped)."""
        return self._archive.get(self.coach_id, {}).get(skill_id)

    def get_all_records(self) -> list[FingerprintArchiveRecord]:
        """Return all records for this coach. ADR-01: only this coach's bucket."""
        return list(self._archive.get(self.coach_id, {}).values())

    # ── Sequence Tracking ──────────────────────────────────────────────────────

    def _next_sequence_for_date(self, compilation_date: date) -> int:
        """Spec §4 Stage 1 Step 3: Assign sequence number starting at 001."""
        date_str = compilation_date.strftime("%Y%m%d")
        coach_bucket = self._archive.get(self.coach_id, {})
        count = sum(
            1 for sid in coach_bucket
            if date_str in sid
        )
        return count + 1

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
