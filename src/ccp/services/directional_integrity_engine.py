"""Directional Integrity Engine — DEP-SDA-020.
Core orchestrator: 4 analyzers, decision router, failure-closed fallback, and domain adapter SDKs."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from src.ccp.models.directional_integrity_models import (
    DirectionalIntegrityDecision as DID, DirectionalIntegrityDecisionSummary,
    DirectionalIntegrityDimension as Dim, DirectionalIntegrityDimensionScore,
    DirectionalIntegrityDomain as Dom, DirectionalIntegrityEngineResult,
    DirectionalIntegrityEvidence, DirectionalIntegrityFallbackReason as FR,
    DirectionalIntegrityReport, DirectionalIntegrityRequest,
    DirectionalIntegrityResolutionPath as RP, DirectionalIntegritySeverity as Sev,
    DirectionalIntegritySurfaceClass as Surf, HardNegativeEvaluationReport,
    PerceptualInteropDecision, SemanticVsPerceptualDecisionState,
    JointRoutingAction, JointFailureClass, PerceptualAttachmentSummary,
    JointFailureSurface, JointValidatorRoutingDecision,
    DirectionalIntegrityInteropReport,
)
from src.ccp.services.directional_integrity_policy_registry import (
    DirectionalIntegrityPolicyRegistry, FORBIDDEN_DRIFTS,
)
from src.ccp.services.hard_negative_adapter import HardNegativeAdapter

def _now() -> datetime: return datetime.now(timezone.utc)
def _id(p: str) -> str: return f"{p}-{uuid4().hex[:8].upper()}"

HIGH_RISK_SURFACES = {Surf.COMMERCIAL_TRUST_TRANSFER, Surf.RENDER_RELEASE, Surf.LONG_FORM_AUTHORITY}

# ── Analyzers ──

class InvariantPreservationAnalyzer:
    """DEP-SDA-022: Scores whether intended existential invariants are preserved."""
    def analyze(self, req: DirectionalIntegrityRequest) -> DirectionalIntegrityDimensionScore:
        field = req.invariant_field
        if not field.primary_invariant_ids:
            return self._score(0.30, "No primary invariants declared — cannot verify preservation", [])
        intensity_values = list(field.invariant_activation_intensity.values())
        avg_intensity = sum(intensity_values) / len(intensity_values) if intensity_values else 0.5
        candidate = req.candidate_text or ""
        inv_mentioned = sum(
            1 for inv_id in field.primary_invariant_ids
            if inv_id.lower() in candidate.lower() or inv_id.lower().replace("_", " ") in candidate.lower()
        )
        coverage = inv_mentioned / len(field.primary_invariant_ids) if field.primary_invariant_ids else 0.0
        score = min(1.0, (avg_intensity * 0.6) + (coverage * 0.4))
        evidence = [DirectionalIntegrityEvidence(
            evidence_id=_id("EVD"), source_kind="invariant_field",
            summary=f"Avg intensity={avg_intensity:.2f}, coverage={coverage:.2f}, primary_count={len(field.primary_invariant_ids)}",
            cited_values={"avg_intensity": avg_intensity, "coverage": coverage},
        )]
        return self._score(score, f"Invariant preservation: {score:.2f}", evidence)

    def _score(self, score, rationale, evidence):
        return DirectionalIntegrityDimensionScore(
            dimension=Dim.INVARIANT_PRESERVATION, score=score,
            severity=Sev.INFO if score >= 0.78 else (Sev.WARNING if score >= 0.62 else Sev.BLOCKING),
            threshold_warning=0.78, threshold_block=0.62, rationale=rationale,
            evidence=evidence, blocking=score < 0.62,
        )


class RepresentationDriftAnalyzer:
    """DEP-SDA-023: Detects encoding/weighting drift against target representation geometry."""
    def analyze(self, req: DirectionalIntegrityRequest) -> DirectionalIntegrityDimensionScore:
        rep = req.representation_geometry
        candidate = (req.candidate_text or "").lower()
        drift_score = 0.0
        drift_reasons = []
        for forbidden in FORBIDDEN_DRIFTS:
            if forbidden in candidate:
                drift_score += 0.20
                drift_reasons.append(forbidden)
        for fd in rep.forbidden_drifts:
            if fd.lower() in candidate:
                drift_score += 0.15
                drift_reasons.append(fd)
        coercion_budget = rep.coercion_risk_budget or 0.5
        if coercion_budget < 0.2 and drift_score > 0.10:
            drift_score += 0.10
        drift_score = min(1.0, drift_score)
        identity_proximity = max(0.0, 1.0 - drift_score)
        evidence = [DirectionalIntegrityEvidence(
            evidence_id=_id("EVD"), source_kind="representation_geometry",
            summary=f"Drift={drift_score:.2f}, reasons={drift_reasons}, identity_proximity={identity_proximity:.2f}",
            cited_values={"drift_score": drift_score, "drift_reasons": drift_reasons, "identity_proximity": identity_proximity},
        )]
        return DirectionalIntegrityDimensionScore(
            dimension=Dim.REPRESENTATION_DRIFT, score=drift_score,
            severity=Sev.INFO if drift_score < 0.28 else (Sev.WARNING if drift_score < 0.45 else Sev.BLOCKING),
            threshold_warning=0.28, threshold_block=0.45, rationale=f"Representation drift: {drift_score:.2f}",
            evidence=evidence, blocking=drift_score >= 0.45,
        )


class HardNegativeAdjacencyAnalyzer:
    """DEP-SDA-024: Scores distance to known deceptive near-neighbors."""
    def __init__(self, adapter: HardNegativeAdapter | None = None) -> None:
        self._adapter = adapter or HardNegativeAdapter()

    def analyze(self, req: DirectionalIntegrityRequest) -> tuple[DirectionalIntegrityDimensionScore, HardNegativeEvaluationReport | None]:
        if not self._adapter.is_available():
            fallback_report = HardNegativeEvaluationReport(
                report_id=_id("HNR"), top_matches=[], strongest_adjacency_score=0.0,
                fallback_reason=FR.MISSING_HARD_NEGATIVE_SERVICE,
            )
            score = DirectionalIntegrityDimensionScore(
                dimension=Dim.HARD_NEGATIVE_ADJACENCY, score=0.0,
                severity=Sev.WARNING, threshold_warning=0.24, threshold_block=0.40,
                rationale="Hard negative service unavailable — scored as unknown",
                evidence=[], blocking=False,
            )
            return score, fallback_report
        hn_report = self._adapter.evaluate(
            candidate_text=req.candidate_text or "",
            representation_geometry_id=req.representation_geometry.representation_geometry_id,
        )
        adj_score = hn_report.strongest_adjacency_score
        candidate = (req.candidate_text or "").lower()
        tokens = candidate.split() if candidate else []
        high_gravity = sum(1 for t in tokens if len(t) > 6) if tokens else 0
        symbolic_density = high_gravity / max(1, len(tokens))
        evidence = [DirectionalIntegrityEvidence(
            evidence_id=_id("EVD"), source_kind="hard_negative",
            summary=f"Strongest adjacency={adj_score:.2f}, matches={len(hn_report.top_matches)}, symbolic_density={symbolic_density:.2f}",
            cited_values={"adjacency": adj_score, "symbolic_density": symbolic_density},
        )]
        return DirectionalIntegrityDimensionScore(
            dimension=Dim.HARD_NEGATIVE_ADJACENCY, score=adj_score,
            severity=Sev.INFO if adj_score < 0.24 else (Sev.WARNING if adj_score < 0.40 else Sev.BLOCKING),
            threshold_warning=0.24, threshold_block=0.40, rationale=f"Hard negative adjacency: {adj_score:.2f}",
            evidence=evidence, blocking=adj_score >= 0.40,
        ), hn_report


class TrajectoryRiskAnalyzer:
    """DEP-SDA-025: Estimates whether downstream meaning trajectory drifts into harmful patterns."""
    RISK_PATTERNS = ["coercive", "dependency", "shame", "exclusion", "manipulation", "vanity", "panic", "guilt-trip"]

    def analyze(self, req: DirectionalIntegrityRequest) -> DirectionalIntegrityDimensionScore:
        candidate = (req.candidate_text or "").lower()
        species = req.species_hypothesis
        risk_score = 0.0
        matched = []
        for pattern in self.RISK_PATTERNS:
            if pattern in candidate:
                risk_score += 0.12
                matched.append(pattern)
        if species and species.shadow_drifts:
            for sd in species.shadow_drifts:
                if sd.lower() in candidate:
                    risk_score += 0.10
                    matched.append(f"shadow:{sd}")
        risk_score = min(1.0, risk_score)
        evidence = [DirectionalIntegrityEvidence(
            evidence_id=_id("EVD"), source_kind="candidate_text",
            summary=f"Trajectory risk={risk_score:.2f}, matched={matched}",
            cited_values={"risk_score": risk_score, "matched_patterns": matched},
        )]
        return DirectionalIntegrityDimensionScore(
            dimension=Dim.TRAJECTORY_RISK, score=risk_score,
            severity=Sev.INFO if risk_score < 0.30 else (Sev.WARNING if risk_score < 0.48 else Sev.BLOCKING),
            threshold_warning=0.30, threshold_block=0.48, rationale=f"Trajectory risk: {risk_score:.2f}",
            evidence=evidence, blocking=risk_score >= 0.48,
        )


# ── Decision Router — DEP-SDA-026 ──

class DirectionalIntegrityDecisionRouter:
    def route(self, *, inv: DirectionalIntegrityDimensionScore, rep: DirectionalIntegrityDimensionScore,
              hn: DirectionalIntegrityDimensionScore, traj: DirectionalIntegrityDimensionScore,
              policy_rules: list, surface: Surf, fallback_reason: FR = FR.NONE,
              hn_service_available: bool = True) -> DirectionalIntegrityDecisionSummary:
        # Apply policy-specific thresholds
        for rule in policy_rules:
            dim_score = {"INVARIANT_PRESERVATION": inv, "REPRESENTATION_DRIFT": rep,
                         "HARD_NEGATIVE_ADJACENCY": hn, "TRAJECTORY_RISK": traj}.get(rule.dimension.value)
            if dim_score:
                dim_score.threshold_warning = rule.warning_threshold
                dim_score.threshold_block = rule.block_threshold
                # Re-evaluate severity based on policy thresholds
                if dim_score.dimension == Dim.INVARIANT_PRESERVATION:
                    dim_score.blocking = dim_score.score < rule.block_threshold
                    dim_score.severity = Sev.INFO if dim_score.score >= rule.warning_threshold else (Sev.WARNING if dim_score.score >= rule.block_threshold else Sev.BLOCKING)
                else:
                    dim_score.blocking = dim_score.score >= rule.block_threshold
                    dim_score.severity = Sev.INFO if dim_score.score < rule.warning_threshold else (Sev.WARNING if dim_score.score < rule.block_threshold else Sev.BLOCKING)

        any_blocking = inv.blocking or rep.blocking or hn.blocking or traj.blocking
        any_warning = inv.severity == Sev.WARNING or rep.severity == Sev.WARNING or hn.severity == Sev.WARNING or traj.severity == Sev.WARNING

        # Dependency fallback enforcement
        if fallback_reason != FR.NONE and surface in HIGH_RISK_SURFACES:
            return DirectionalIntegrityDecisionSummary(
                decision=DID.FAIL, resolution_path=RP.HARD_BLOCK, blocking=True, advisory_only=False,
                summary=f"Fail-closed: dependency degraded ({fallback_reason.value}) on high-risk surface {surface.value}",
            )
        if fallback_reason != FR.NONE:
            return DirectionalIntegrityDecisionSummary(
                decision=DID.REVIEW, resolution_path=RP.OPERATOR_REVIEW, blocking=False, advisory_only=False,
                summary=f"Review required: dependency degraded ({fallback_reason.value}) on {surface.value}",
            )

        if any_blocking:
            return DirectionalIntegrityDecisionSummary(
                decision=DID.FAIL, resolution_path=RP.HARD_BLOCK, blocking=True, advisory_only=False,
                summary="Blocking dimension threshold exceeded",
            )
        if any_warning:
            path = RP.REGENERATE if surface == Surf.RENDER_RELEASE else RP.OPERATOR_REVIEW
            return DirectionalIntegrityDecisionSummary(
                decision=DID.REVIEW, resolution_path=path, blocking=False, advisory_only=False,
                summary="Warning threshold exceeded on one or more dimensions",
            )
        return DirectionalIntegrityDecisionSummary(
            decision=DID.PASS, resolution_path=RP.CONTINUE, blocking=False, advisory_only=True,
            summary="All dimensions within acceptable thresholds",
        )


# ── Main Engine — DEP-SDA-020 ──

class DirectionalIntegrityEngine:
    def __init__(self, *, policy_registry: DirectionalIntegrityPolicyRegistry | None = None,
                 hard_negative_adapter: HardNegativeAdapter | None = None,
                 receipt_chain: Any = None) -> None:
        self._policy = policy_registry or DirectionalIntegrityPolicyRegistry()
        self._hn_adapter = hard_negative_adapter or HardNegativeAdapter()
        self._receipt = receipt_chain
        self._inv_analyzer = InvariantPreservationAnalyzer()
        self._rep_analyzer = RepresentationDriftAnalyzer()
        self._hn_analyzer = HardNegativeAdjacencyAnalyzer(self._hn_adapter)
        self._traj_analyzer = TrajectoryRiskAnalyzer()
        self._router = DirectionalIntegrityDecisionRouter()

    def evaluate(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
        if self._receipt:
            self._receipt.log(action="di-evaluation-started", metadata={"request_id": request.request_id})

        # Null packet check
        if not request.invariant_field or not request.archetypal_geometry or not request.representation_geometry:
            return self._fail_closed(request, FR.NULL_RUNTIME_PACKET, "Null or incomplete runtime packets")

        # Policy resolution
        policy = self._policy.resolve(request.domain, request.surface_class)
        if not policy:
            if request.surface_class in HIGH_RISK_SURFACES:
                return self._fail_closed(request, FR.MISSING_POLICY, "Missing policy for high-risk surface")
            return self._fail_closed(request, FR.MISSING_POLICY, "Missing policy bundle", decision=DID.REVIEW)

        if self._receipt:
            self._receipt.log(action="di-policy-resolved", metadata={"policy_id": policy.policy_id})

        # Run analyzers
        inv_score = self._inv_analyzer.analyze(request)
        rep_score = self._rep_analyzer.analyze(request)
        hn_score, hn_report = self._hn_analyzer.analyze(request)
        traj_score = self._traj_analyzer.analyze(request)

        # Determine fallback reason
        fallback = FR.NONE
        dep_warnings = []
        if not self._hn_adapter.is_available():
            fallback = FR.MISSING_HARD_NEGATIVE_SERVICE
            dep_warnings.append("Hard negative service unavailable")

        # Route decision
        decision = self._router.route(
            inv=inv_score, rep=rep_score, hn=hn_score, traj=traj_score,
            policy_rules=policy.rules, surface=request.surface_class,
            fallback_reason=fallback, hn_service_available=self._hn_adapter.is_available(),
        )

        # Build corrections list
        corrections = []
        if inv_score.blocking:
            corrections.append(f"Strengthen invariant preservation (current: {inv_score.score:.2f}, required: >={inv_score.threshold_block:.2f})")
        if rep_score.blocking:
            corrections.append(f"Reduce representation drift (current: {rep_score.score:.2f}, required: <{rep_score.threshold_block:.2f})")
        if hn_score.blocking:
            corrections.append(f"Address hard-negative adjacency (current: {hn_score.score:.2f}, required: <{hn_score.threshold_block:.2f})")
        if traj_score.blocking:
            corrections.append(f"Mitigate trajectory risk (current: {traj_score.score:.2f}, required: <{traj_score.threshold_block:.2f})")

        # Resonance multiplier from invariant field
        resonance = {}
        if request.invariant_field.invariant_resonance_multiplier_hint:
            resonance = request.invariant_field.invariant_resonance_multiplier_hint

        # Symbolic density from HN evidence
        symbolic_density = None
        if hn_score.evidence:
            for ev in hn_score.evidence:
                if "symbolic_density" in ev.cited_values:
                    symbolic_density = ev.cited_values["symbolic_density"]

        # Identity proximity from rep evidence
        identity_proximity = None
        if rep_score.evidence:
            for ev in rep_score.evidence:
                if "identity_proximity" in ev.cited_values:
                    identity_proximity = ev.cited_values["identity_proximity"]

        overall = (inv_score.score * 0.3 + (1.0 - rep_score.score) * 0.25 + (1.0 - hn_score.score) * 0.25 + (1.0 - traj_score.score) * 0.2)

        report = DirectionalIntegrityReport(
            report_id=_id("DIR"), request_id=request.request_id,
            domain=request.domain, surface_class=request.surface_class,
            policy_id=policy.policy_id, evaluated_at_utc=_now(),
            decision_summary=decision,
            invariant_preservation_score=inv_score, representation_drift_score=rep_score,
            hard_negative_adjacency_score=hn_score, trajectory_risk_score=traj_score,
            overall_confidence=min(1.0, max(0.0, overall)),
            invariant_resonance_multiplier=resonance,
            symbolic_density=symbolic_density, identity_proximity=identity_proximity,
            hard_negative_report=hn_report, fallback_reason=fallback,
            dependency_warnings=dep_warnings, required_corrections=corrections,
            lineage_refs=[request.invariant_field.packet_id, request.archetypal_geometry.packet_id, request.representation_geometry.representation_geometry_id],
        )

        should_circuit_break = (decision.decision == DID.FAIL and request.surface_class in HIGH_RISK_SURFACES and (rep_score.blocking or hn_score.blocking))

        result = DirectionalIntegrityEngineResult(
            report=report,
            should_continue_automation=decision.decision == DID.PASS,
            should_queue_operator_review=decision.decision == DID.REVIEW,
            should_trigger_regeneration=decision.resolution_path == RP.REGENERATE,
            should_trip_circuit_break=should_circuit_break,
        )

        if self._receipt:
            self._receipt.log(action="di-evaluation-complete", metadata={
                "request_id": request.request_id, "decision": decision.decision.value,
                "resolution": decision.resolution_path.value, "policy_id": policy.policy_id,
                "inv": inv_score.score, "rep": rep_score.score, "hn": hn_score.score, "traj": traj_score.score,
            })

        return result

    def compose_interop_report(
        self,
        semantic_report: DirectionalIntegrityReport,
        perceptual_attachment: Optional[PerceptualAttachmentSummary] = None,
    ) -> DirectionalIntegrityInteropReport:
        if self._receipt:
            self._receipt.log(
                action="interop-composition-started",
                metadata={"semantic_report_id": semantic_report.report_id}
            )

        # 1. Resolve decisions
        sem_decision = semantic_report.decision_summary.decision
        if perceptual_attachment is None:
            per_decision = PerceptualInteropDecision.MISSING
        else:
            per_decision = perceptual_attachment.perceptual_decision

        # 2. Form state enum
        state_str = f"SEMANTIC_{sem_decision.value}__PERCEPTUAL_{per_decision.value}"
        combined_state = SemanticVsPerceptualDecisionState(state_str)

        # 3. Determine failure class
        if sem_decision == DID.FAIL:
            if per_decision in (PerceptualInteropDecision.DOWNGRADE, PerceptualInteropDecision.BLOCK):
                failure_class = JointFailureClass.MIXED_FAILURE
            else:
                failure_class = JointFailureClass.SEMANTIC_FAILURE
        elif sem_decision == DID.REVIEW:
            if per_decision in (PerceptualInteropDecision.REVIEW, PerceptualInteropDecision.DOWNGRADE, PerceptualInteropDecision.BLOCK):
                failure_class = JointFailureClass.MIXED_FAILURE
            elif per_decision == PerceptualInteropDecision.MISSING:
                failure_class = JointFailureClass.MIXED_FAILURE
            else:
                failure_class = JointFailureClass.SEMANTIC_FAILURE
        else:  # PASS
            if per_decision in (PerceptualInteropDecision.REVIEW, PerceptualInteropDecision.DOWNGRADE, PerceptualInteropDecision.BLOCK):
                failure_class = JointFailureClass.PERCEPTUAL_FAILURE
            elif per_decision == PerceptualInteropDecision.MISSING:
                failure_class = JointFailureClass.MISSING_PERCEPTUAL_PREREQUISITE
            else:
                failure_class = JointFailureClass.NONE

        # 4. Resolve policy-aware action
        surface = semantic_report.surface_class
        is_high_risk = surface in HIGH_RISK_SURFACES

        if sem_decision == DID.FAIL:
            action = JointRoutingAction.HARD_BLOCK
        elif sem_decision == DID.REVIEW:
            if per_decision == PerceptualInteropDecision.BLOCK:
                action = JointRoutingAction.HARD_BLOCK
            else:
                action = JointRoutingAction.OPERATOR_REVIEW
        else:  # PASS
            if per_decision == PerceptualInteropDecision.PASS:
                action = JointRoutingAction.CONTINUE
            elif per_decision == PerceptualInteropDecision.REVIEW:
                if surface == Surf.RENDER_RELEASE:
                    action = JointRoutingAction.REGENERATE
                else:
                    action = JointRoutingAction.OPERATOR_REVIEW
            elif per_decision == PerceptualInteropDecision.DOWNGRADE:
                if surface == Surf.COMMERCIAL_TRUST_TRANSFER:
                    action = JointRoutingAction.HARD_BLOCK
                else:
                    action = JointRoutingAction.DOWNGRADE_SURFACE
            elif per_decision == PerceptualInteropDecision.BLOCK:
                action = JointRoutingAction.HARD_BLOCK
            elif per_decision == PerceptualInteropDecision.MISSING:
                if is_high_risk:
                    action = JointRoutingAction.HOLD_FOR_PERCEPTUAL_PREREQUISITE
                else:
                    action = JointRoutingAction.CONTINUE

        # 5. Resolve flags
        should_trip_circuit_break = (
            (sem_decision == DID.FAIL and is_high_risk and (
                semantic_report.representation_drift_score.blocking or
                semantic_report.hard_negative_adjacency_score.blocking
            )) or
            action == JointRoutingAction.CIRCUIT_BREAK
        )

        should_continue_automation = (
            action == JointRoutingAction.CONTINUE or
            (action == JointRoutingAction.DOWNGRADE_SURFACE and not is_high_risk)
        )

        should_queue_operator_review = (
            action == JointRoutingAction.OPERATOR_REVIEW or
            action == JointRoutingAction.HOLD_FOR_PERCEPTUAL_PREREQUISITE
        )

        should_trigger_regeneration = action == JointRoutingAction.REGENERATE

        # 6. Populate failure surface details
        semantic_failure_present = sem_decision != DID.PASS
        perceptual_failure_present = per_decision in (
            PerceptualInteropDecision.REVIEW,
            PerceptualInteropDecision.DOWNGRADE,
            PerceptualInteropDecision.BLOCK
        )
        missing_perceptual_prerequisite = per_decision == PerceptualInteropDecision.MISSING

        blocking_reasons = []
        required_corrections = []
        summary_msg = f"Semantic {sem_decision.value}, Perceptual {per_decision.value} -> {action.value}"

        if semantic_failure_present:
            blocking_reasons.extend(semantic_report.required_corrections)
            required_corrections.extend(semantic_report.required_corrections)

        if perceptual_failure_present or missing_perceptual_prerequisite:
            if per_decision == PerceptualInteropDecision.MISSING:
                msg = f"Perceptual prerequisite missing on high-risk surface {surface.value}"
                if is_high_risk:
                    blocking_reasons.append(msg)
                required_corrections.append("Run perceptual influence evaluation and attach the result.")
            else:
                msg = f"Perceptual evaluation returned {per_decision.value}"
                blocking_reasons.append(msg)
                required_corrections.append(f"Resolve perceptual issues resulting in {per_decision.value}.")

        if perceptual_attachment:
            dependency_warnings = (
                list(semantic_report.dependency_warnings) +
                list(perceptual_attachment.dependency_warnings)
            )
            lineage_refs = list(dict.fromkeys(
                list(semantic_report.lineage_refs) +
                list(perceptual_attachment.lineage_refs)
            ))
            if perceptual_attachment.required_corrections:
                required_corrections.extend(perceptual_attachment.required_corrections)
        else:
            dependency_warnings = list(semantic_report.dependency_warnings)
            lineage_refs = list(semantic_report.lineage_refs)

        failure_surface = JointFailureSurface(
            failure_class=failure_class,
            combined_state=combined_state,
            semantic_failure_present=semantic_failure_present,
            perceptual_failure_present=perceptual_failure_present,
            missing_perceptual_prerequisite=missing_perceptual_prerequisite,
            summary=summary_msg,
            blocking_reasons=blocking_reasons,
            required_corrections=required_corrections,
        )

        routing_decision = JointValidatorRoutingDecision(
            action=action,
            should_continue_automation=should_continue_automation,
            should_queue_operator_review=should_queue_operator_review,
            should_trigger_regeneration=should_trigger_regeneration,
            should_trip_circuit_break=should_trip_circuit_break,
            explanation=f"Joint routing action is {action.value} due to combined state {combined_state.value}",
        )

        interop_report = DirectionalIntegrityInteropReport(
            interop_report_id=_id("DIR-INT"),
            semantic_report_id=semantic_report.report_id,
            semantic_decision=sem_decision.value,
            combined_state=combined_state,
            semantic_report_generated_at_utc=semantic_report.evaluated_at_utc,
            perceptual_attachment=perceptual_attachment,
            failure_surface=failure_surface,
            routing_decision=routing_decision,
            lineage_refs=lineage_refs,
            dependency_warnings=dependency_warnings,
        )

        if self._receipt:
            self._receipt.log(
                action="interop-composition-complete",
                metadata={
                    "interop_report_id": interop_report.interop_report_id,
                    "combined_state": combined_state.value,
                    "action": action.value
                }
            )

        return interop_report

    def evaluate_interop(
        self,
        request: DirectionalIntegrityRequest,
        perceptual_attachment: Optional[PerceptualAttachmentSummary] = None,
    ) -> DirectionalIntegrityInteropReport:
        sem_result = self.evaluate(request)
        return self.compose_interop_report(sem_result.report, perceptual_attachment)


    def _fail_closed(self, request, fallback_reason, summary, decision=DID.FAIL):
        null_dim = lambda dim: DirectionalIntegrityDimensionScore(
            dimension=dim, score=0.0, severity=Sev.BLOCKING, threshold_warning=0.0,
            threshold_block=0.0, rationale=summary, evidence=[], blocking=True,
        )
        dec_summary = DirectionalIntegrityDecisionSummary(
            decision=decision, resolution_path=RP.HARD_BLOCK if decision == DID.FAIL else RP.OPERATOR_REVIEW,
            blocking=decision == DID.FAIL, advisory_only=False, summary=summary,
        )
        report = DirectionalIntegrityReport(
            report_id=_id("DIR"), request_id=request.request_id,
            domain=request.domain, surface_class=request.surface_class,
            policy_id="NONE", evaluated_at_utc=_now(), decision_summary=dec_summary,
            invariant_preservation_score=null_dim(Dim.INVARIANT_PRESERVATION),
            representation_drift_score=null_dim(Dim.REPRESENTATION_DRIFT),
            hard_negative_adjacency_score=null_dim(Dim.HARD_NEGATIVE_ADJACENCY),
            trajectory_risk_score=null_dim(Dim.TRAJECTORY_RISK),
            overall_confidence=0.0, fallback_reason=fallback_reason,
            dependency_warnings=[summary], required_corrections=[summary],
        )
        return DirectionalIntegrityEngineResult(
            report=report, should_continue_automation=False,
            should_queue_operator_review=decision == DID.REVIEW,
            should_trigger_regeneration=False, should_trip_circuit_break=decision == DID.FAIL,
        )


# ── Domain Adapter SDKs (Phase D) ──

class DIServiceClient:
    """SDK for upstream semantic planning boundaries (CCF integration target)."""
    def __init__(self, engine: DirectionalIntegrityEngine) -> None:
        self._engine = engine
    def validate_for_planning(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
        request.surface_class = Surf.SEMANTIC_PLANNING
        return self._engine.evaluate(request)

class DIRenderReleaseGuard:
    """SDK for media generation boundaries (CMF integration target)."""
    def __init__(self, engine: DirectionalIntegrityEngine) -> None:
        self._engine = engine
    def validate_for_release(self, request: DirectionalIntegrityRequest) -> DirectionalIntegrityEngineResult:
        request.surface_class = Surf.RENDER_RELEASE
        return self._engine.evaluate(request)

def map_surface_payload(domain: Dom, request: DirectionalIntegrityRequest) -> DirectionalIntegrityRequest:
    """Surface-class helper: maps domain intent to standard validation payload."""
    surface_map = {
        Dom.CCF: Surf.SEMANTIC_PLANNING,
        Dom.CMF: Surf.RENDER_RELEASE,
        Dom.CBCS: Surf.COACHING_INTERVENTION,
        Dom.REACTIONS: Surf.SOCIAL_REACTION,
        Dom.WEBINAR: Surf.LONG_FORM_AUTHORITY,
        Dom.COMMERCIAL: Surf.COMMERCIAL_TRUST_TRANSFER,
    }
    request.surface_class = surface_map.get(domain, Surf.SEMANTIC_PLANNING)
    request.domain = domain
    return request
