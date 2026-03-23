"""
FR48 — Forensic Audit Protocol Service (DEP-ENG-042)
Skill fingerprint registration + asset binding + forensic reconstruction.

AC1: SKILL-{ARCH}-{COACH}-{MOOD}-{FRAME}-{COHORT}-{DATE}-{SEQ} syntax.
AC2: Asset binding to fingerprint.
AC3: Dependency hashing (dep_snapshot).
AC4: Forensic reconstruction via trace_lineage.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.cross_system_models import (
    AudienceCohort,
    ForensicLineage,
    MoodState,
    ReceiptBlock,
    RegulatoryFrame,
    SkillContext,
    SkillFingerprintID,
)


class ForensicAuditService:
    """
    FR48: Forensic audit protocol — skill fingerprint + lineage tracing.
    """

    def __init__(self, coach_acronym: str) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(f"coach_acronym must be 2-4 chars, got '{coach_acronym}'")
        self._coach = coach_acronym.upper()
        self._receipt_chain = ReceiptChain(coach_acronym=self._coach)
        # In-memory fingerprint store (production: Supabase fingerprint_archive)
        self._fingerprints: dict[str, SkillFingerprintID] = {}
        # Asset → fingerprint bindings
        self._bindings: dict[str, str] = {}
        self._sequence_counter: int = 0

    # ── AC1: Skill Fingerprint Syntax ──────────────────

    def generate_skill_fingerprint(
        self,
        *,
        archetype_template_id: str,
        mood: MoodState,
        regulatory_frame: RegulatoryFrame,
        audience_cohort: AudienceCohort,
        tmt_function: str = "",
        sdt_need_primary: str = "",
        dep_versions: Optional[dict[str, str]] = None,
    ) -> SkillFingerprintID:
        """
        FR48 AC1: Generate SKILL-{ARCH}-{COACH}-{MOOD}-{FRAME}-{COHORT}-{DATE}-{SEQ}.
        """
        self._sequence_counter += 1
        date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
        seq = f"{self._sequence_counter:04d}"

        skill_id = (
            f"SKILL-{archetype_template_id}-{self._coach}-"
            f"{mood.value}-{regulatory_frame.value}-"
            f"{audience_cohort.value}-{date_str}-{seq}"
        )

        # AC3: Dependency hashing
        dep_snapshot: dict[str, str] = {}
        if dep_versions:
            for dep_key, dep_val in dep_versions.items():
                dep_hash = hashlib.sha256(dep_val.encode()).hexdigest()[:16]
                dep_snapshot[dep_key] = dep_hash

        context = SkillContext(
            coach_id=self._coach,
            mood_state=mood,
            regulatory_frame=regulatory_frame,
            audience_cohort=audience_cohort,
            tmt_function=tmt_function,
            sdt_need_primary=sdt_need_primary,
        )

        fingerprint = SkillFingerprintID(
            skill_id=skill_id,
            archetype_template_id=archetype_template_id,
            context=context,
            dep_snapshot=dep_snapshot,
        )

        self._fingerprints[skill_id] = fingerprint

        self._receipt_chain.log(
            agent_id="ForensicAuditService",
            action="SKILL_FINGERPRINT_GENERATED",
            asset_id=skill_id,
            decision="SUCCESS",
            decision_rationale=f"mood={mood.value}, frame={regulatory_frame.value}",
        )

        return fingerprint

    # ── AC2: Asset Binding ─────────────────────────────

    def bind_asset_to_fingerprint(
        self,
        *,
        asset_id: str,
        skill_fingerprint_id: str,
    ) -> bool:
        """
        FR48 AC2: Bind an asset to its skill fingerprint.
        """
        if skill_fingerprint_id not in self._fingerprints:
            return False

        fingerprint = self._fingerprints[skill_fingerprint_id]
        fingerprint.outputs.append(asset_id)
        self._bindings[asset_id] = skill_fingerprint_id

        self._receipt_chain.log(
            agent_id="ForensicAuditService",
            action="ASSET_BOUND_TO_FINGERPRINT",
            asset_id=asset_id,
            decision="SUCCESS",
            decision_rationale=f"fingerprint={skill_fingerprint_id}",
        )

        return True

    # ── AC4: Forensic Reconstruction ───────────────────

    def trace_lineage(
        self,
        asset_id: str,
        receipt_chain: Optional[list[ReceiptBlock]] = None,
    ) -> Optional[ForensicLineage]:
        """
        FR48 AC4: Full forensic reconstruction for an asset.
        """
        fingerprint_id = self._bindings.get(asset_id)
        if not fingerprint_id:
            return None

        fingerprint = self._fingerprints.get(fingerprint_id)
        if not fingerprint:
            return None

        # Extract agent sequence from receipt chain
        agent_sequence: list[str] = []
        if receipt_chain:
            agent_sequence = [b.executing_agent for b in receipt_chain]

        lineage = ForensicLineage(
            asset_id=asset_id,
            skill_fingerprint_id=fingerprint_id,
            context=fingerprint.context,
            agent_sequence=agent_sequence,
            receipt_chain=receipt_chain or [],
        )

        self._receipt_chain.log(
            agent_id="ForensicAuditService",
            action="LINEAGE_TRACED",
            asset_id=asset_id,
            decision="SUCCESS",
            decision_rationale=f"fingerprint={fingerprint_id}, agents={len(agent_sequence)}",
        )

        return lineage

    # ── Queries ────────────────────────────────────────

    def get_fingerprint(self, skill_id: str) -> Optional[SkillFingerprintID]:
        return self._fingerprints.get(skill_id)

    def get_fingerprint_for_asset(self, asset_id: str) -> Optional[SkillFingerprintID]:
        fp_id = self._bindings.get(asset_id)
        if fp_id:
            return self._fingerprints.get(fp_id)
        return None

    @property
    def fingerprint_count(self) -> int:
        return len(self._fingerprints)
