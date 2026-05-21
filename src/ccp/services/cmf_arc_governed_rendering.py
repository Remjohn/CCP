from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

# Import existing models
from src.ccp.models.cmf_arc_render_models import (
    ArcRenderJobRecord, ArcRenderJobStatus, ArcRenderManifest, ArcRenderReleaseResult,
    BeatClusterPlan, BeatClusterType, ClusterShotDirective, CoalitionSpineInput,
    DeterministicControlSpec, EpicMeaningGateResult, EpicMeaningVerdict,
    FirstFrameAuthorityCheck, FirstFrameVerdict, ShotGrammarProfile, TempoEnvelope,
)

# Import new SFL render models
from src.ccp.models.cmf_sfl_render_models import (
    RenderSurfaceType, CompositionDepthMode, VariationHintMode,
    TemporalRelationType, RenderFallbackDecision, ScoreCardVisibleScore,
    ScoreCardRenderBundle, AuditBoardRenderBundle, TemporalCraftHint,
    TemporalCraftHints, CompositionDepthRenderProfile, VariationRenderHints,
    RenderPerceptualPlan, PreservationDimensionResult, RenderPreservationReport,
)

# Import related SFL & Perceptual models
from src.ccp.models.sfl_query_models import SubliminalFunctionStackPacket
from src.ccp.models.perceptual_influence_models import PerceptualInfluenceReport, PerceptualInfluenceDecision

def _now() -> datetime: return datetime.now(timezone.utc)
def _id(p: str) -> str: return f"{p}-{uuid4().hex[:8].upper()}"

# ── Arc-type to shot grammar mapping ──
ARC_SHOT_MAP: dict[str, tuple[BeatClusterType, ShotGrammarProfile]] = {
    "rally": (BeatClusterType.rally, ShotGrammarProfile.kinetic_escalation),
    "witness": (BeatClusterType.witness, ShotGrammarProfile.intimate_observation),
    "reflection": (BeatClusterType.reflection, ShotGrammarProfile.contemplative_pause),
    "confrontation": (BeatClusterType.confrontation, ShotGrammarProfile.pressure_lock),
}

ARC_SHOT_DIRECTIVES: dict[BeatClusterType, ClusterShotDirective] = {
    BeatClusterType.rally: ClusterShotDirective(camera_distance="medium-wide pull to close-up", lighting_profile="high-contrast dramatic side-key with warm fill", movement_profile="accelerating push-in with handheld energy", transition_profile="hard-cut on beat accent", symbolic_environment="movement stage, rally floor, open arena"),
    BeatClusterType.witness: ClusterShotDirective(camera_distance="intimate close-up", lighting_profile="soft directional key with deep shadow fall-off", movement_profile="slow dolly or locked tripod stillness", transition_profile="dissolve with breath-sync pacing", symbolic_environment="quiet interior, personal workspace, window light"),
    BeatClusterType.reflection: ClusterShotDirective(camera_distance="medium shot with negative space", lighting_profile="diffused cool tone with single practical source", movement_profile="static or imperceptible drift", transition_profile="long dissolve or fade to silence", symbolic_environment="solitary environment, landscape edge, dusk"),
    BeatClusterType.confrontation: ClusterShotDirective(camera_distance="tight close-up to extreme close-up", lighting_profile="harsh split lighting with minimal fill", movement_profile="locked frame with tension hold", transition_profile="smash-cut on confrontation beat", symbolic_environment="confined space, high-stakes interior, spotlight isolation"),
}

ARC_TEMPO: dict[BeatClusterType, TempoEnvelope] = {
    BeatClusterType.rally: TempoEnvelope(bpm_start=110, bpm_peak=140, bpm_end=120, silence_windows_ms=[]),
    BeatClusterType.witness: TempoEnvelope(bpm_start=70, bpm_peak=85, bpm_end=65, silence_windows_ms=[2000]),
    BeatClusterType.reflection: TempoEnvelope(bpm_start=55, bpm_peak=65, bpm_end=50, silence_windows_ms=[3000, 2000]),
    BeatClusterType.confrontation: TempoEnvelope(bpm_start=95, bpm_peak=130, bpm_end=80, silence_windows_ms=[1500]),
}

ARC_NARRATIVE_PURPOSE: dict[BeatClusterType, str] = {
    BeatClusterType.rally: "Build escalating conviction through kinetic energy and momentum toward a collective call-to-action",
    BeatClusterType.witness: "Hold intimate space for authentic testimony and personal evidence of transformation",
    BeatClusterType.reflection: "Create contemplative pause allowing the audience to internalize the meaning before the next beat",
    BeatClusterType.confrontation: "Apply direct pressure to a false belief or competing narrative with unflinching clarity",
}

CORPORATE_ANTI_PATTERNS = ["corporate aesthetics", "sterile lighting", "posed expressions", "corporate blandness", "flat even lighting", "stock photography aesthetic"]

class NarrativeRenderingModel:
    def translate(self, spine: CoalitionSpineInput) -> list[BeatClusterPlan]:
        arc_key = spine.somatic_arc_type.lower().replace(" ", "_").replace("-", "_")
        if arc_key not in ARC_SHOT_MAP:
            arc_key = "witness"
        cluster_type, shot_grammar = ARC_SHOT_MAP[arc_key]
        segments = [s.strip() for s in spine.spine_text.split(".") if s.strip()]
        if not segments:
            segments = [spine.spine_text]
        clusters: list[BeatClusterPlan] = []
        ms_per_seg = max(3000, 60000 // max(1, len(segments)))
        for i, seg in enumerate(segments):
            clusters.append(BeatClusterPlan(
                cluster_id=_id("CLU"), cluster_type=cluster_type, order_index=i,
                start_ms=i * ms_per_seg, end_ms=(i + 1) * ms_per_seg,
                shot_grammar=shot_grammar, shot_directive=ARC_SHOT_DIRECTIVES[cluster_type],
                tempo_envelope=ARC_TEMPO[cluster_type],
                deterministic_controls=DeterministicControlSpec(
                    first_frame_spec_id=_id("FFS"), conscious_pose_id=_id("CPOSE"),
                    conscious_smile_preset="authentic_intensity", identity_lora_path=f"lora/{spine.voice_dna_id}/identity.safetensors",
                    gaze_rule="direct-to-camera with intentional break on cluster transition",
                ),
                narrative_purpose=ARC_NARRATIVE_PURPOSE[cluster_type],
            ))
        return clusters

class BeatClusterPlanner:
    def plan(self, clusters: list[BeatClusterPlan]) -> list[BeatClusterPlan]:
        for i, c in enumerate(clusters):
            c.order_index = i
        return sorted(clusters, key=lambda c: c.order_index)

class OmniShotBoundaryPlanner:
    def compute_boundaries(self, clusters: list[BeatClusterPlan]) -> list[dict]:
        boundaries = []
        for i in range(len(clusters) - 1):
            boundaries.append({"from_cluster": clusters[i].cluster_id, "to_cluster": clusters[i + 1].cluster_id, "cut_ms": clusters[i].end_ms, "transition": clusters[i].shot_directive.transition_profile})
        return boundaries

class ArcSonicBedPlanner:
    def plan_sonic(self, clusters: list[BeatClusterPlan]) -> list[TempoEnvelope]:
        return [c.tempo_envelope for c in clusters]

class ArcGovernedVCBAugmentor:
    def augment(self, *, spine: CoalitionSpineInput, clusters: list[BeatClusterPlan]) -> dict:
        return {"content_output_id": spine.content_output_id, "coach_id": spine.coach_id, "selected_format": spine.selected_format, "cluster_directives": [{"cluster_id": c.cluster_id, "shot_grammar": c.shot_grammar.value, "lighting": c.shot_directive.lighting_profile, "environment": c.shot_directive.symbolic_environment} for c in clusters]}

class DeterministicControlResolver:
    def resolve(self, *, cluster: BeatClusterPlan, voice_dna_id: str) -> DeterministicControlSpec:
        return DeterministicControlSpec(
            first_frame_spec_id=cluster.deterministic_controls.first_frame_spec_id,
            conscious_pose_id=cluster.deterministic_controls.conscious_pose_id,
            conscious_smile_preset=cluster.deterministic_controls.conscious_smile_preset,
            identity_lora_path=f"lora/{voice_dna_id}/identity.safetensors",
            gaze_rule=cluster.deterministic_controls.gaze_rule,
        )

class FirstFrameAuthorityGate:
    AUTHORITY_THRESHOLD = 0.72
    CONTRAST_THRESHOLD = 0.65
    RECOGNIZABILITY_THRESHOLD = 0.70

    def evaluate(self, *, cluster: BeatClusterPlan, authority_score: float = 0.80, contrast_score: float = 0.75, recognizability_score: float = 0.80, anti_generic_flags: list[str] | None = None) -> FirstFrameAuthorityCheck:
        flags = anti_generic_flags or []
        corporate_flags = [f for f in flags if any(p in f.lower() for p in CORPORATE_ANTI_PATTERNS)]
        score_pass = (authority_score >= self.AUTHORITY_THRESHOLD and contrast_score >= self.CONTRAST_THRESHOLD and recognizability_score >= self.RECOGNIZABILITY_THRESHOLD)
        if corporate_flags or not score_pass:
            verdict = FirstFrameVerdict.fail
        else:
            verdict = FirstFrameVerdict.pass_
        return FirstFrameAuthorityCheck(check_id=_id("FFC"), cluster_id=cluster.cluster_id, verdict=verdict, authority_score=authority_score, contrast_score=contrast_score, recognizability_score=recognizability_score, anti_generic_flags=flags, checked_at=_now())

class EpicMeaningGate:
    BLANDNESS_PASS_THRESHOLD = 0.15
    BLANDNESS_ESCALATE_THRESHOLD = 0.30

    def evaluate(self, *, job_id: str, blandness_confidence: float = 0.05, failed_rules: list[str] | None = None, has_cluster_tempo: bool = True) -> EpicMeaningGateResult:
        rules = failed_rules or []
        if not has_cluster_tempo:
            rules.append("generic_sonic_bed_without_cluster_tempo")
        corporate_rules = [r for r in rules if any(p in r.lower() for p in CORPORATE_ANTI_PATTERNS)]
        if blandness_confidence > self.BLANDNESS_ESCALATE_THRESHOLD or corporate_rules:
            verdict = EpicMeaningVerdict.fail_corporate_aesthetic
            rationale = f"Corporate aesthetic detected. Blandness={blandness_confidence:.2f}. Rules: {', '.join(rules)}"
        elif blandness_confidence > self.BLANDNESS_PASS_THRESHOLD:
            verdict = EpicMeaningVerdict.escalate
            rationale = f"Blandness borderline ({blandness_confidence:.2f}). Manual review recommended."
        elif not has_cluster_tempo:
            verdict = EpicMeaningVerdict.fail_generic_sonic_bed
            rationale = "Sonic bed lacks cluster-specific tempo or silence windows."
        elif rules:
            verdict = EpicMeaningVerdict.fail_flat_lighting
            rationale = f"Visual grammar violations: {', '.join(rules)}"
        else:
            verdict = EpicMeaningVerdict.pass_
            rationale = "Preview passes Epic Meaning Framing. Crusade intensity confirmed."
        return EpicMeaningGateResult(gate_id=_id("EMG"), job_id=job_id, verdict=verdict, blandness_confidence=blandness_confidence, failed_rules=rules, rationale=rationale, checked_at=_now())

class RenderReleaseGate:
    def can_release(self, *, first_frame: FirstFrameAuthorityCheck | None, epic_meaning: EpicMeaningGateResult | None, perceptual_plan: RenderPerceptualPlan | None = None, perceptual_report: PerceptualInfluenceReport | None = None) -> tuple[bool, str]:
        if first_frame is None: return False, "First frame check not completed"
        if first_frame.verdict != FirstFrameVerdict.pass_: return False, f"First frame failed: {first_frame.verdict.value}"
        if epic_meaning is None: return False, "Epic Meaning gate not completed"
        if epic_meaning.verdict != EpicMeaningVerdict.pass_: return False, f"Epic Meaning failed: {epic_meaning.verdict.value}"
        
        # SFL Additions
        if perceptual_plan is not None:
            surface = perceptual_plan.surface_type
            if surface in (RenderSurfaceType.REEL, RenderSurfaceType.COURSE_VIDEO, RenderSurfaceType.AUDIT_CARD, RenderSurfaceType.AUDIT_BOARD):
                if perceptual_report is None:
                    return False, f"Missing PerceptualInfluenceReport on high-risk surface: {surface.value}"
                
                # Check evaluator decision if present (AC-12-SFL.6: CMF consumes report and decisions)
                if perceptual_report.decision_summary.decision == PerceptualInfluenceDecision.DOWNGRADE:
                    pass
                elif perceptual_report.decision_summary.decision in ("BLOCK", "FAIL"):
                    return False, "PerceptualInfluenceReport decision is BLOCK/FAIL"

        return True, "Both gates passed"

class SkiaRenderManifestBuilder:
    def build(self, *, job_id: str, spine: CoalitionSpineInput, vcb_id: str, clusters: list[BeatClusterPlan]) -> ArcRenderManifest:
        return ArcRenderManifest(manifest_id=_id("MAN"), job_id=job_id, content_output_id=spine.content_output_id, selected_format=spine.selected_format, vcb_id=vcb_id, beat_clusters=clusters, render_target_path=f"renders/{job_id}/output", created_at=_now())

class SkiaRenderSidecarBridge:
    def __init__(self, sidecar_path: str = "src/ccp/sidecars/skia-renderer/") -> None:
        self._path = sidecar_path
    def submit(self, manifest: ArcRenderManifest) -> dict:
        return {"manifest_id": manifest.manifest_id, "status": "submitted", "sidecar_path": self._path}
    def poll_status(self, manifest_id: str) -> dict:
        return {"manifest_id": manifest_id, "status": "completed"}

class CMFArcGovernedRenderingPipeline:
    def __init__(self, receipt_chain: Any = None, canvas_service: Any = None, vcb_generator: Any = None, supabase_client: Any = None) -> None:
        self._receipt = receipt_chain
        self._canvas = canvas_service
        self._vcb = vcb_generator
        self._sb = supabase_client
        self._nrm = NarrativeRenderingModel()
        self._planner = BeatClusterPlanner()
        self._shot_boundary = OmniShotBoundaryPlanner()
        self._sonic = ArcSonicBedPlanner()
        self._augmentor = ArcGovernedVCBAugmentor()
        self._ff_gate = FirstFrameAuthorityGate()
        self._em_gate = EpicMeaningGate()
        self._release_gate = RenderReleaseGate()
        self._manifest_builder = SkiaRenderManifestBuilder()
        self._sidecar = SkiaRenderSidecarBridge()

    def create_job(
        self,
        spine: CoalitionSpineInput,
        surface_type: RenderSurfaceType = RenderSurfaceType.SINGLE_IMAGE,
        sfl_stack: SubliminalFunctionStackPacket | None = None,
        directional_report_id: str = "DIR-DEFAULT",
        perceptual_report: PerceptualInfluenceReport | None = None,
    ) -> ArcRenderJobRecord:
        clusters = self._nrm.translate(spine)
        clusters = self._planner.plan(clusters)
        self._shot_boundary.compute_boundaries(clusters)
        self._sonic.plan_sonic(clusters)
        job_id = _id("ARJ")
        now = _now()
        # First frame gate on first cluster
        ff_check = self._ff_gate.evaluate(cluster=clusters[0]) if clusters else None
        status = ArcRenderJobStatus.planned
        if ff_check and ff_check.verdict != FirstFrameVerdict.pass_:
            status = ArcRenderJobStatus.first_frame_blocked
        elif ff_check:
            status = ArcRenderJobStatus.preview_rendering
        
        # Build Perceptual Plan if SFL structures are present
        perceptual_plan = None
        if sfl_stack is not None:
            if perceptual_report is None:
                raise ValueError("Missing PerceptualInfluenceReport: cannot generate RenderPerceptualPlan")
            perceptual_plan = self.build_render_perceptual_plan(
                content_output_id=spine.content_output_id,
                coach_id=spine.coach_id,
                surface_type=surface_type,
                sfl_stack=sfl_stack,
                directional_report_id=directional_report_id,
                perceptual_report=perceptual_report
            )

        job = ArcRenderJobRecord(job_id=job_id, content_output_id=spine.content_output_id, coach_id=spine.coach_id, status=status, selected_format=spine.selected_format, beat_clusters=clusters, first_frame_check=ff_check, created_at=now, updated_at=now)
        
        # Keep references dynamic
        job.perceptual_plan = perceptual_plan
        job.perceptual_report = perceptual_report

        if self._receipt: self._receipt.log(action="arc-render-job-created", metadata={"job_id": job_id, "status": status.value})
        return job

    def build_composition_depth_profile(self, surface_type: RenderSurfaceType) -> CompositionDepthRenderProfile:
        if surface_type == RenderSurfaceType.SINGLE_IMAGE:
            return CompositionDepthRenderProfile(
                profile_id=_id("CDP"),
                surface_type=surface_type,
                repetition_with_variation_weight=0.1,
                layered_interpretation_weight=0.7,
                rhythmic_structure_weight=0.1,
                strategic_ambiguity_weight=0.1,
                preserve_subtext=True,
                allow_explicit_exposition=False
            )
        elif surface_type == RenderSurfaceType.CAROUSEL:
            return CompositionDepthRenderProfile(
                profile_id=_id("CDP"),
                surface_type=surface_type,
                repetition_with_variation_weight=0.7,
                layered_interpretation_weight=0.1,
                rhythmic_structure_weight=0.1,
                strategic_ambiguity_weight=0.1,
                preserve_subtext=True,
                allow_explicit_exposition=False
            )
        elif surface_type in (RenderSurfaceType.REEL, RenderSurfaceType.COURSE_VIDEO):
            return CompositionDepthRenderProfile(
                profile_id=_id("CDP"),
                surface_type=surface_type,
                repetition_with_variation_weight=0.2,
                layered_interpretation_weight=0.2,
                rhythmic_structure_weight=0.5,
                strategic_ambiguity_weight=0.1,
                preserve_subtext=True,
                allow_explicit_exposition=False
            )
        else: # e.g. AUDIT_CARD, AUDIT_BOARD, AUDIT_EXPLAINER
            return CompositionDepthRenderProfile(
                profile_id=_id("CDP"),
                surface_type=surface_type,
                repetition_with_variation_weight=0.2,
                layered_interpretation_weight=0.2,
                rhythmic_structure_weight=0.2,
                strategic_ambiguity_weight=0.4,
                preserve_subtext=True,
                allow_explicit_exposition=True
            )

    def build_variation_render_hints(self, surface_type: RenderSurfaceType) -> VariationRenderHints:
        if surface_type == RenderSurfaceType.SINGLE_IMAGE:
            return VariationRenderHints(
                hint_id=_id("VRH"),
                surface_type=surface_type,
                asymmetry_balance_target=0.8,
                resonance_carry_target=0.3,
                salience_distribution_target=0.9,
                paradox_retention_target=0.4,
                predictability_break_target=0.2,
                notes=["Single image layout optimization"]
            )
        elif surface_type == RenderSurfaceType.CAROUSEL:
            return VariationRenderHints(
                hint_id=_id("VRH"),
                surface_type=surface_type,
                asymmetry_balance_target=0.6,
                resonance_carry_target=0.7,
                salience_distribution_target=0.6,
                paradox_retention_target=0.5,
                predictability_break_target=0.8,
                notes=["Slide-to-slide variation carry-over"]
            )
        elif surface_type in (RenderSurfaceType.REEL, RenderSurfaceType.COURSE_VIDEO):
            return VariationRenderHints(
                hint_id=_id("VRH"),
                surface_type=surface_type,
                asymmetry_balance_target=0.5,
                resonance_carry_target=0.8,
                salience_distribution_target=0.7,
                paradox_retention_target=0.6,
                predictability_break_target=0.7,
                notes=["Temporal dynamic pacing cuts"]
            )
        else: # e.g. AUDIT_CARD, AUDIT_BOARD
            return VariationRenderHints(
                hint_id=_id("VRH"),
                surface_type=surface_type,
                asymmetry_balance_target=0.4,
                resonance_carry_target=0.5,
                salience_distribution_target=0.5,
                paradox_retention_target=0.7,
                predictability_break_target=0.4,
                notes=["Readable data visualization layout"]
            )

    def build_temporal_craft_hints(self, surface_type: RenderSurfaceType, sfl_stack: SubliminalFunctionStackPacket | None) -> TemporalCraftHints:
        hints_list = []
        rhythm = "Standard rhythm"
        if sfl_stack:
            for i, fn_id in enumerate(sfl_stack.active_function_ids):
                rel = TemporalRelationType.TRANSITION
                if i % 3 == 0:
                    rel = TemporalRelationType.HARD_CUT
                elif "SUDDEN" in fn_id:
                    rel = TemporalRelationType.SUDDEN_JUMP_RISK
                
                hints_list.append(TemporalCraftHint(
                    cluster_id=f"CLU-{i}",
                    relation_type=rel,
                    cut_ms=3000 + i * 500,
                    hold_ms=1000 + i * 200,
                    pause_weight_ms=500 + i * 100,
                    transition_label="crossfade" if rel == TemporalRelationType.TRANSITION else "cut",
                    sudden_jump_risk=0.1 * i,
                    interpretability_note=f"Pacing adjusted for SFL function {fn_id}"
                ))
            rhythm = f"SFL governed rhythm with {len(sfl_stack.active_function_ids)} active functions"
        else:
            rhythm = "Downgraded flat pacing"

        return TemporalCraftHints(
            hint_set_id=_id("TCH"),
            source_video_asset_id="VIDEO-001",
            hints=hints_list,
            rhythm_summary=rhythm
        )

    def build_render_perceptual_plan(
        self,
        content_output_id: str,
        coach_id: str,
        surface_type: RenderSurfaceType,
        sfl_stack: SubliminalFunctionStackPacket,
        directional_report_id: str,
        perceptual_report: PerceptualInfluenceReport,
        target_thumbnail_count: int = 4,
    ) -> RenderPerceptualPlan:
        depth_profile = self.build_composition_depth_profile(surface_type)
        variation_hints = self.build_variation_render_hints(surface_type)
        temporal_hints = self.build_temporal_craft_hints(surface_type, sfl_stack)
        plan_id = _id("RPP")
        
        card_safe = surface_type in (RenderSurfaceType.AUDIT_CARD, RenderSurfaceType.AUDIT_BOARD)
        pdf_safe = surface_type == RenderSurfaceType.AUDIT_BOARD

        plan = RenderPerceptualPlan(
            plan_id=plan_id,
            content_output_id=content_output_id,
            coach_id=coach_id,
            surface_type=surface_type,
            function_stack_packet_id=sfl_stack.packet_id,
            directional_integrity_report_id=directional_report_id,
            perceptual_influence_report_id=perceptual_report.report_id,
            depth_profile=depth_profile,
            variation_hints=variation_hints,
            temporal_hints=temporal_hints,
            target_thumbnail_count=target_thumbnail_count,
            card_safe=card_safe,
            pdf_safe=pdf_safe,
            generated_at=_now(),
        )

        if self._sb:
            try:
                self._sb.table("cmf_render_perceptual_plans").insert({
                    "plan_id": plan.plan_id,
                    "content_output_id": plan.content_output_id,
                    "coach_id": plan.coach_id,
                    "surface_type": plan.surface_type.value,
                    "function_stack_packet_id": plan.function_stack_packet_id,
                    "directional_integrity_report_id": plan.directional_integrity_report_id,
                    "perceptual_influence_report_id": plan.perceptual_influence_report_id,
                    "depth_profile_json": plan.depth_profile.model_dump(),
                    "variation_hints_json": plan.variation_hints.model_dump(),
                    "temporal_hints_json": plan.temporal_hints.model_dump(),
                    "target_thumbnail_count": plan.target_thumbnail_count,
                    "card_safe": plan.card_safe,
                    "pdf_safe": plan.pdf_safe,
                    "generated_at": plan.generated_at.isoformat(),
                }).execute()
            except Exception as e:
                print(f"Failed to insert perceptual plan into Supabase: {e}")

        if self._receipt:
            self._receipt.log(
                action="render-perceptual-plan-created",
                metadata={"plan_id": plan_id, "surface_type": surface_type.value}
            )
        return plan

    def generate_audit_bundles(
        self,
        job: ArcRenderJobRecord,
        plan: RenderPerceptualPlan,
        report: PerceptualInfluenceReport,
    ) -> tuple[ScoreCardRenderBundle, AuditBoardRenderBundle]:
        thumbnail_id = f"THUMB-{plan.content_output_id}-001"
        mb = report.metric_bundle
        visible_scores = [
            ScoreCardVisibleScore(label="Cognitive Imprint", score_0_99=int(mb.cognitive_imprint_score.score * 99)),
            ScoreCardVisibleScore(label="Symbolic Density", score_0_99=int(mb.symbolic_density_score.score * 99)),
            ScoreCardVisibleScore(label="Human Congruence", score_0_99=int(mb.human_congruence_score.score * 99)),
            ScoreCardVisibleScore(label="Contrast Clarity", score_0_99=int(mb.contrast_clarity_score.score * 99)),
            ScoreCardVisibleScore(label="Memorability Pressure", score_0_99=int(mb.memorability_pressure.score * 99)),
            ScoreCardVisibleScore(label="Overexplanation Risk", score_0_99=int(mb.overexplanation_risk_score.score * 99)),
        ]
        overall_score = int(report.influence_alignment.alignment_score * 99)
        ai_slop_risk = int(mb.synthetic_smoothness_score.score * 99)
        verdict = report.decision_summary.rationale or "Crusade intensity confirmed."

        card = ScoreCardRenderBundle(
            card_id=f"CARD-{job.job_id}",
            content_thumbnail_asset_id=thumbnail_id,
            surface_type=plan.surface_type,
            overall_score_0_99=overall_score,
            ai_slop_risk_0_99=ai_slop_risk,
            visible_scores=visible_scores,
            verdict_line=verdict,
            format_ratio=job.selected_format
        )
        
        board = AuditBoardRenderBundle(
            board_id=f"BOARD-{job.job_id}",
            card_ids=[card.card_id],
            hero_thumbnail_asset_id=thumbnail_id,
            board_layout_template_id="layout-standard-2x3",
            page_count=1,
            export_targets=["pdf", "image"]
        )

        # Saliency analysis fallback rule integration
        review_flag = False
        try:
            from src.ccp.services.saliency_analysis_service import SaliencyAnalysisService
            saliency_service = SaliencyAnalysisService(coach_acronym="CCH", receipt_chain=self._receipt)
            img_url = f"https://s3.amazonaws.com/ccp-assets/{plan.content_output_id}/keyframe.png"
            analysis, override, status = saliency_service.analyze(
                image_url=img_url,
                image_type="character_specific_emotion"
            )
            if status == "PENDING_HUMAN_REVIEW" or analysis.confidence < 0.7:
                review_flag = True
        except Exception:
            review_flag = True

        if review_flag:
            card.verdict_line += " [Requires Saliency Review]"

        if self._receipt:
            self._receipt.log(
                action="score-card-bundle-generated",
                metadata={"card_id": card.card_id, "board_id": board.board_id}
            )
        return card, board

    def build_preservation_report(
        self,
        plan: RenderPerceptualPlan,
        report: PerceptualInfluenceReport,
        manifest_id: str = "",
    ) -> RenderPreservationReport:
        dimensions = []
        lost_intents = []
        downgraded_surfaces = []
        mb = report.metric_bundle
        
        dims_to_check = [
            ("COGNITIVE_IMPRINT", mb.cognitive_imprint_score.score),
            ("SYMBOLIC_DENSITY", mb.symbolic_density_score.score),
            ("HUMAN_CONGRUENCE", mb.human_congruence_score.score),
            ("CONTRAST_CLARITY", mb.contrast_clarity_score.score),
            ("MEMORABILITY_PRESSURE", mb.memorability_pressure.score),
        ]
        
        fallback_decision = RenderFallbackDecision.PASS
        for name, score in dims_to_check:
            realized = score
            if mb.synthetic_smoothness_score.score > 0.4:
                realized = max(0.0, score - 0.15)
                lost_intents.append(f"Reduced clarity on {name} due to high synthetic smoothness risk.")
                fallback_decision = RenderFallbackDecision.DOWNGRADE
                
            preserved = (realized >= score - 0.05)
            dimensions.append(PreservationDimensionResult(
                dimension_name=name,
                intended_level=score,
                realized_level=realized,
                preserved=preserved,
                rationale=f"Dimension {name} preserved." if preserved else f"Dimension {name} suffered slight quality loss."
            ))
            
        if fallback_decision == RenderFallbackDecision.DOWNGRADE:
            downgraded_surfaces.append(plan.surface_type.value)

        pres_report = RenderPreservationReport(
            report_id=_id("RPR"),
            plan_id=plan.plan_id,
            manifest_id=manifest_id,
            fallback_decision=fallback_decision,
            dimensions=dimensions,
            lost_intents=lost_intents,
            downgraded_surfaces=downgraded_surfaces,
            reviewer_notes=["Automatic evaluation of rendering preservation completed."],
            created_at=_now()
        )

        if self._sb:
            try:
                self._sb.table("cmf_render_preservation_reports").insert({
                    "report_id": pres_report.report_id,
                    "plan_id": pres_report.plan_id,
                    "manifest_id": pres_report.manifest_id,
                    "fallback_decision": pres_report.fallback_decision.value,
                    "dimensions_json": [d.model_dump() for d in pres_report.dimensions],
                    "lost_intents": pres_report.lost_intents,
                    "downgraded_surfaces": pres_report.downgraded_surfaces,
                    "reviewer_notes": pres_report.reviewer_notes,
                    "created_at": pres_report.created_at.isoformat(),
                }).execute()
            except Exception as e:
                print(f"Failed to insert preservation report into Supabase: {e}")

        if self._receipt:
            self._receipt.log(
                action="render-preservation-report-generated",
                metadata={"report_id": pres_report.report_id, "fallback_decision": fallback_decision.value}
            )
        return pres_report

    def run_epic_meaning_gate(self, job: ArcRenderJobRecord, *, blandness_confidence: float = 0.05, failed_rules: list[str] | None = None, has_cluster_tempo: bool = True) -> ArcRenderJobRecord:
        em = self._em_gate.evaluate(job_id=job.job_id, blandness_confidence=blandness_confidence, failed_rules=failed_rules, has_cluster_tempo=has_cluster_tempo)
        job.epic_meaning_gate = em
        if em.verdict == EpicMeaningVerdict.pass_:
            job.status = ArcRenderJobStatus.full_rendering
        else:
            job.status = ArcRenderJobStatus.preview_failed
        job.updated_at = _now()
        if self._receipt: self._receipt.log(action="epic-meaning-gate-evaluated", metadata={"job_id": job.job_id, "verdict": em.verdict.value})
        return job

    def build_manifest(self, job: ArcRenderJobRecord, spine: CoalitionSpineInput, vcb_id: str) -> ArcRenderManifest:
        manifest = self._manifest_builder.build(job_id=job.job_id, spine=spine, vcb_id=vcb_id, clusters=job.beat_clusters)
        job.manifest_id = manifest.manifest_id
        job.status = ArcRenderJobStatus.ready_for_composition
        job.updated_at = _now()
        
        # Build preservation report if perceptual plan is present
        perceptual_plan = getattr(job, "perceptual_plan", None)
        perceptual_report = getattr(job, "perceptual_report", None)
        if perceptual_plan and perceptual_report:
            job.preservation_report = self.build_preservation_report(
                plan=perceptual_plan,
                report=perceptual_report,
                manifest_id=manifest.manifest_id
            )
        return manifest

    def release(self, job: ArcRenderJobRecord) -> ArcRenderReleaseResult | None:
        perceptual_plan = getattr(job, "perceptual_plan", None)
        perceptual_report = getattr(job, "perceptual_report", None)
        can, reason = self._release_gate.can_release(
            first_frame=job.first_frame_check,
            epic_meaning=job.epic_meaning_gate,
            perceptual_plan=perceptual_plan,
            perceptual_report=perceptual_report
        )
        if not can:
            if self._receipt: self._receipt.log(action="release-denied", metadata={"job_id": job.job_id, "reason": reason})
            return None
        job.status = ArcRenderJobStatus.released
        job.updated_at = _now()
        receipt_id = _id("RCP")
        if self._receipt: self._receipt.log(action="arc-render-released", metadata={"job_id": job.job_id, "receipt_id": receipt_id})
        return ArcRenderReleaseResult(job_id=job.job_id, composition_id=job.composition_id or _id("COMP"), release_receipt_id=receipt_id, released_at=_now())
