from __future__ import annotations
from typing import Optional
from uuid import uuid4
from datetime import datetime, timezone
from src.ccp.models.cbcs_models import (
    CbcsPerceptualIntakeEnvelope,
    VisibleScoreCarryover,
    ScoreBand,
    PerceptualSeverity,
    VisibleScoreName,
    PerceptualEffectSummary,
    PerceptualWeaknessSignal,
    PerceptualStrengthSignal,
    PerceptualSourceReference,
    SourceSystem,
    CardEvidenceSnapshot,
    AuditPrescriptionItem,
    AuditIntelligenceSummaryInput,
)
from src.ccp.models.perceptual_influence_models import PerceptualInfluenceReport


class CbcsSflAdapter:
    """Adapter to map FR-27 Perceptual Influence reports and provisional FR-35 audit summaries
    into the canonical CbcsPerceptualIntakeEnvelope structure."""

    @staticmethod
    def map_score_to_band(score_val: int, rationale: str) -> ScoreBand:
        if score_val < 25:
            severity = PerceptualSeverity.CRITICAL
        elif score_val < 45:
            severity = PerceptualSeverity.HIGH
        elif score_val < 65:
            severity = PerceptualSeverity.MODERATE
        else:
            severity = PerceptualSeverity.LOW
        return ScoreBand(score_0_99=score_val, severity=severity, rationale=rationale)

    @classmethod
    def from_fr27_report(
        cls,
        report: PerceptualInfluenceReport,
        client_id: str,
        coach_id: str,
        card_snapshot: Optional[CardEvidenceSnapshot] = None,
        audit_prescriptions: Optional[list[AuditPrescriptionItem]] = None,
    ) -> CbcsPerceptualIntakeEnvelope:
        mb = report.metric_bundle

        humanity_val = int(mb.human_congruence_score.score * 99)
        presence_val = int(mb.cognitive_imprint_score.score * 99)
        trust_val = int(mb.contrast_clarity_score.score * 99)
        memorability_val = int(mb.memorability_pressure.score * 99)
        resonance_val = int(mb.symbolic_density_score.score * 99)
        signal_val = int(mb.contrast_clarity_score.score * 99)
        slop_val = int(mb.synthetic_smoothness_score.score * 99)

        visible_scores = VisibleScoreCarryover(
            humanity=cls.map_score_to_band(humanity_val, mb.human_congruence_score.explanation),
            presence=cls.map_score_to_band(presence_val, mb.cognitive_imprint_score.explanation),
            trust=cls.map_score_to_band(trust_val, mb.contrast_clarity_score.explanation),
            memorability=cls.map_score_to_band(memorability_val, mb.memorability_pressure.explanation),
            resonance=cls.map_score_to_band(resonance_val, mb.symbolic_density_score.explanation),
            signal=cls.map_score_to_band(signal_val, mb.contrast_clarity_score.explanation),
            ai_slop_risk=cls.map_score_to_band(slop_val, mb.synthetic_smoothness_score.explanation),
        )

        primary_weaknesses: list[PerceptualWeaknessSignal] = []
        primary_strengths: list[PerceptualStrengthSignal] = []

        for name in VisibleScoreName:
            band: ScoreBand = getattr(visible_scores, name.value)
            if name == VisibleScoreName.AI_SLOP_RISK:
                if band.score_0_99 >= 45:
                    primary_weaknesses.append(
                        PerceptualWeaknessSignal(
                            signal_id=f"weak-{name.value}-{uuid4().hex[:6]}",
                            score_name=name,
                            severity=band.severity,
                            label="Elevated AI Slop Risk",
                            description=band.rationale,
                            coaching_implication="De-smooth content, increase rawness and grounded humanness.",
                        )
                    )
            else:
                if band.score_0_99 < 45:
                    primary_weaknesses.append(
                        PerceptualWeaknessSignal(
                            signal_id=f"weak-{name.value}-{uuid4().hex[:6]}",
                            score_name=name,
                            severity=band.severity,
                            label=f"Low {name.value.capitalize()}",
                            description=band.rationale,
                            coaching_implication=f"Focus on improving {name.value.capitalize()} via tailored coaching drills.",
                        )
                    )
                elif band.score_0_99 >= 80:
                    primary_strengths.append(
                        PerceptualStrengthSignal(
                            signal_id=f"strong-{name.value}-{uuid4().hex[:6]}",
                            score_name=name,
                            severity=band.severity,
                            label=f"Strong {name.value.capitalize()}",
                            description=band.rationale,
                            preservation_note=f"Reinforce and maintain {name.value.capitalize()} without flattening it.",
                        )
                    )

        anti_slop = slop_val >= 45
        synthetic_tone = report.false_depth_result.detected or (slop_val >= 45)

        effect_summary = PerceptualEffectSummary(
            summary_id=f"pes-{uuid4().hex[:6]}",
            primary_weaknesses=primary_weaknesses,
            primary_strengths=primary_strengths,
            anti_slop_warning_active=anti_slop,
            synthetic_tone_risk_active=synthetic_tone,
            recommendation_hint=report.decision_summary.rationale or "Calibrate for audience resonance",
        )

        source_ref = PerceptualSourceReference(
            source_system=SourceSystem.FR27,
            source_contract_id=report.report_id,
            source_artifact_id=report.request_id,
            source_version="1.0.0",
            generated_at_utc=report.evaluated_at_utc.isoformat(),
        )

        return CbcsPerceptualIntakeEnvelope(
            envelope_id=f"env-{uuid4().hex[:6]}",
            coach_id=coach_id,
            client_id=client_id,
            visible_scores=visible_scores,
            effect_summary=effect_summary,
            source_reference=source_ref,
            card_snapshot=card_snapshot,
            audit_prescriptions=audit_prescriptions or [],
        )

    @classmethod
    def from_fr35_audit(
        cls,
        audit_input: AuditIntelligenceSummaryInput,
        client_id: str,
        coach_id: str,
    ) -> CbcsPerceptualIntakeEnvelope:
        """Provisional adapter for future FR-35 Audit Intelligence summary inputs."""
        return CbcsPerceptualIntakeEnvelope(
            envelope_id=f"env-{uuid4().hex[:6]}",
            coach_id=coach_id,
            client_id=client_id,
            visible_scores=audit_input.visible_scores,
            effect_summary=audit_input.effect_summary,
            source_reference=audit_input.source_reference,
            card_snapshot=audit_input.card_snapshot,
            audit_prescriptions=audit_input.prescription_items,
        )
