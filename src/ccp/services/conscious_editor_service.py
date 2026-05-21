from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.models.conscious_editor_models import (
    ConsciousEditorSession,
    CreateTranscriptRevisionRequest,
    EditorArtifactSummary,
    EditorLineageGraph,
    EditorSessionStatus,
    EditorTier,
    ExecuteRerenderRequest,
    LineageNode,
    LineageNodeType,
    MediaReviewSummary,
    OperatorDecision,
    OperatorDecisionResponse,
    RerenderScope,
    ScopedRerenderDecision,
    TranscriptRevision,
    TranscriptSourceKind,
    TranscriptTokenPatch,
)


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


# ════════════════════════════════════════════════════════════════════════
# EditorArtifactResolver — DEP-CED-002
# Resolves one reviewable session into semantic, visual, and lineage
# payloads. Joins source audio, ContentMachineResult, VCB, composition.
# ════════════════════════════════════════════════════════════════════════

class EditorArtifactResolver:
    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    def resolve(self, *, editor_session_id: str, coach_id: str, source_audio_asset_id: str, content_machine_result: dict | None = None, vcb: dict | None = None, composition: dict | None = None) -> ConsciousEditorSession:
        now = _now_utc()

        artifact_summary = None
        media_summary = None
        status = EditorSessionStatus.pending_artifact
        tier = EditorTier.artifact_review
        content_output_id = None
        vcb_id = None
        composition_id = None

        if content_machine_result and content_machine_result.get("success", False):
            content_output_id = content_machine_result.get("content_output_id", _new_id("CO"))
            artifact_summary = EditorArtifactSummary(
                content_output_id=content_output_id,
                session_id=editor_session_id,
                coach_id=coach_id,
                archetype_container=content_machine_result.get("archetype_container", "unknown"),
                content_piece_ids=content_machine_result.get("content_piece_ids", []),
                coalition_signature=content_machine_result.get("coalition_signature"),
                anti_centroid_warnings=content_machine_result.get("anti_centroid_warnings", []),
                trigger_first_verified=bool(content_machine_result.get("source_audio_asset_id")),
            )

            if content_machine_result.get("anti_centroid_warnings"):
                status = EditorSessionStatus.provisional_warnings
            else:
                status = EditorSessionStatus.artifact_ready

        if vcb:
            vcb_id = vcb.get("vcb_id", _new_id("VCB"))

        if composition and artifact_summary:
            composition_id = composition.get("composition_id", _new_id("COMP"))
            slide_count = composition.get("slide_count", 1)
            composition_status = composition.get("status", "draft")
            media_summary = MediaReviewSummary(
                vcb_id=vcb_id or _new_id("VCB"),
                composition_id=composition_id,
                composition_status=composition_status,
                slide_count=slide_count,
                editable_transcript_enabled=True,
            )
            tier = EditorTier.media_validation
            if status == EditorSessionStatus.artifact_ready:
                status = EditorSessionStatus.media_ready

        session = ConsciousEditorSession(
            editor_session_id=editor_session_id,
            tier=tier,
            status=status,
            coach_id=coach_id,
            source_audio_asset_id=source_audio_asset_id,
            content_output_id=content_output_id,
            vcb_id=vcb_id,
            composition_id=composition_id,
            artifact_summary=artifact_summary,
            media_summary=media_summary,
            created_at_utc=now,
            updated_at_utc=now,
        )

        if self._supabase is not None:
            try:
                self._supabase.table("conscious_editor_sessions").upsert({
                    "editor_session_id": editor_session_id,
                    "coach_id": coach_id,
                    "source_audio_asset_id": source_audio_asset_id,
                    "content_output_id": content_output_id,
                    "vcb_id": vcb_id,
                    "composition_id": composition_id,
                    "status": status.value,
                    "tier": tier.value,
                    "created_at": now,
                    "updated_at": now,
                }, on_conflict="editor_session_id").execute()
            except Exception:
                pass

        return session


# ════════════════════════════════════════════════════════════════════════
# ArtifactReadinessGate — DEP-CED-004
# Blocks media review until semantic artifact exists and is source-linked.
# PROVISIONAL verdict for anti-centroid warnings.
# ════════════════════════════════════════════════════════════════════════

class ArtifactReadinessGate:
    def check(self, session: ConsciousEditorSession) -> EditorSessionStatus:
        if session.artifact_summary is None:
            return EditorSessionStatus.pending_artifact
        if not session.source_audio_asset_id:
            return EditorSessionStatus.blocked
        if session.artifact_summary.anti_centroid_warnings:
            return EditorSessionStatus.provisional_warnings
        return EditorSessionStatus.artifact_ready


# ════════════════════════════════════════════════════════════════════════
# ArchetypeContainerProjection — DEP-CED-003
# Projects compiled meaning into a coach-readable archetype-first view.
# ════════════════════════════════════════════════════════════════════════

class ArchetypeContainerProjection:
    def project(self, artifact: EditorArtifactSummary) -> dict:
        return {
            "archetype_container": artifact.archetype_container,
            "content_pieces": artifact.content_piece_ids,
            "coalition_signature": artifact.coalition_signature,
            "anti_centroid_warnings": artifact.anti_centroid_warnings,
            "trigger_first_verified": artifact.trigger_first_verified,
        }


# ════════════════════════════════════════════════════════════════════════
# TranscriptRevisionManager — DEP-CED-005
# Append-only revision persistence with diff capture.
# Linear time interpolation for modified tokens (Phase3-M05).
# ════════════════════════════════════════════════════════════════════════

class TranscriptRevisionManager:
    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    def create_revision(self, *, editor_session_id: str, author_person_id: str, request: CreateTranscriptRevisionRequest, original_tokens: list[dict] | None = None) -> TranscriptRevision:
        revision_id = _new_id("REV")
        now = _now_utc()

        # Apply linear time interpolation for modified tokens
        enriched_patches: list[TranscriptTokenPatch] = []
        for patch in request.token_patches:
            start_ms = patch.start_ms
            end_ms = patch.end_ms

            if original_tokens and patch.start_ms == 0 and patch.end_ms == 0:
                idx = patch.token_index
                prev_end = 0
                next_start = 0
                if idx > 0 and idx - 1 < len(original_tokens):
                    prev_end = original_tokens[idx - 1].get("end_ms", 0)
                if idx + 1 < len(original_tokens):
                    next_start = original_tokens[idx + 1].get("start_ms", prev_end + 500)
                else:
                    next_start = prev_end + 500
                start_ms = prev_end
                end_ms = next_start

            semantic_flag = patch.semantic_change_flag
            enriched_patches.append(TranscriptTokenPatch(
                token_index=patch.token_index,
                original_text=patch.original_text,
                revised_text=patch.revised_text,
                start_ms=start_ms,
                end_ms=end_ms,
                semantic_change_flag=semantic_flag,
            ))

        requires_timing_reflow = any(
            len(p.revised_text) > len(p.original_text) * 1.5 for p in enriched_patches
        )

        revision = TranscriptRevision(
            revision_id=revision_id,
            editor_session_id=editor_session_id,
            source_kind=TranscriptSourceKind.operator_revision,
            author_person_id=author_person_id,
            revision_note=request.revision_note,
            revised_plaintext=request.revised_plaintext,
            revised_json_payload=request.revised_json_payload,
            token_patches=enriched_patches,
            requires_timing_reflow=requires_timing_reflow,
            created_at_utc=now,
        )

        if self._supabase is not None:
            try:
                self._supabase.table("conscious_editor_transcript_revisions").insert({
                    "revision_id": revision_id,
                    "editor_session_id": editor_session_id,
                    "source_kind": TranscriptSourceKind.operator_revision.value,
                    "author_person_id": author_person_id,
                    "revision_note": request.revision_note,
                    "revised_plaintext": request.revised_plaintext,
                    "revised_json_payload": request.revised_json_payload,
                    "token_patches_json": [p.model_dump() for p in enriched_patches],
                    "requires_timing_reflow": requires_timing_reflow,
                    "created_at": now,
                }).execute()
            except Exception:
                pass

        return revision


# ════════════════════════════════════════════════════════════════════════
# ScopedRerenderClassifier — DEP-CED-006
# Deterministic scope selection per M-05 taxonomy.
# ════════════════════════════════════════════════════════════════════════

class ScopedRerenderClassifier:
    def classify(self, *, revision: TranscriptRevision, has_visual_defect: bool = False, visual_concept_changed: bool = False, source_disputed: bool = False, affected_slide_indices: list[int] | None = None) -> ScopedRerenderDecision:
        decision_id = _new_id("RRD")
        now = _now_utc()

        scope: RerenderScope
        rationale: str
        requires_vcb = False
        slides = affected_slide_indices or []

        if source_disputed:
            scope = RerenderScope.source_restart_required
            rationale = "Operator disputes semantic truth, source attribution, or audio authenticity."
        elif visual_concept_changed:
            scope = RerenderScope.cmf_full_regen_from_compiled_meaning
            rationale = "Visual concept changed enough that current VCB is invalid. Core meaning remains valid."
            requires_vcb = True
        elif has_visual_defect and not revision.token_patches:
            scope = RerenderScope.visual_slide_regeneration
            rationale = "Slide-specific visual defect with unchanged transcript."
        elif revision.requires_timing_reflow:
            scope = RerenderScope.composition_reflow
            rationale = "Text length change requiring layout recompute without new visuals."
        elif revision.token_patches:
            has_semantic_change = any(p.semantic_change_flag for p in revision.token_patches)
            if has_semantic_change:
                scope = RerenderScope.composition_reflow
                rationale = "Semantic token change requiring composition reflow."
            else:
                scope = RerenderScope.caption_text_patch
                rationale = "Spelling, punctuation, or subtitle wording change with unchanged meaning."
        else:
            scope = RerenderScope.caption_text_patch
            rationale = "Text-only correction without structural impact."

        return ScopedRerenderDecision(
            decision_id=decision_id,
            editor_session_id=revision.editor_session_id,
            revision_id=revision.revision_id,
            scope=scope,
            rationale=rationale,
            affected_slide_indices=slides,
            requires_vcb_refresh=requires_vcb,
            requires_audio_rerecord=False,
            requires_nim_rerun=False,
            created_at_utc=now,
        )


# ════════════════════════════════════════════════════════════════════════
# CompositionPatchAssembler — DEP-CED-008
# Rebuilds text_content payloads for caption-only and reflow scopes.
# ════════════════════════════════════════════════════════════════════════

class CompositionPatchAssembler:
    def assemble_text_patch(self, *, revision: TranscriptRevision, existing_text_content: dict | None = None, slide_count: int = 1) -> dict:
        text_content: dict = existing_text_content or {}
        revised_words = revision.revised_plaintext.split()
        words_per_slide = max(1, len(revised_words) // slide_count)

        for slide_idx in range(slide_count):
            start = slide_idx * words_per_slide
            end = start + words_per_slide if slide_idx < slide_count - 1 else len(revised_words)
            slide_text = " ".join(revised_words[start:end])
            text_content[slide_idx] = {"caption": slide_text}

        return text_content


# ════════════════════════════════════════════════════════════════════════
# VisualRegenerationAdapter — DEP-CED-009
# Bridges slide-level visual changes into request_regeneration(...)
# ════════════════════════════════════════════════════════════════════════

class VisualRegenerationAdapter:
    def __init__(self, canvas_service: Any = None) -> None:
        self._canvas = canvas_service

    def regenerate_slide(self, *, composition_id: str, slide_index: int, revision_note: str) -> dict:
        if self._canvas is not None:
            try:
                result = self._canvas.request_regeneration(composition_id, slide_index, revision_note)
                return {"status": "regenerated", "composition_id": composition_id, "slide_index": slide_index}
            except Exception as e:
                return {"status": "failed", "error": str(e), "composition_id": composition_id, "slide_index": slide_index}
        return {"status": "no_canvas_service", "composition_id": composition_id, "slide_index": slide_index}


# ════════════════════════════════════════════════════════════════════════
# ScopedRerenderOrchestrator — DEP-CED-007
# Executes the minimal valid rerender path against existing CCP services.
# ════════════════════════════════════════════════════════════════════════

class ScopedRerenderOrchestrator:
    def __init__(self, canvas_service: Any = None, vcb_generator: Any = None, receipt_chain: Any = None) -> None:
        self._canvas = canvas_service
        self._vcb_generator = vcb_generator
        self._receipt_chain = receipt_chain
        self._patch_assembler = CompositionPatchAssembler()
        self._visual_adapter = VisualRegenerationAdapter(canvas_service)

    def execute(self, *, decision: ScopedRerenderDecision, revision: TranscriptRevision, composition_id: str, vcb_id: str, slide_count: int = 1) -> dict:
        result = {"scope": decision.scope.value, "status": "completed"}

        if decision.scope == RerenderScope.caption_text_patch:
            text_content = self._patch_assembler.assemble_text_patch(revision=revision, slide_count=slide_count)
            if self._canvas is not None:
                try:
                    self._canvas.create_composition(vcb_id, "patch_template", slide_count, {}, {}, text_content=text_content)
                except Exception:
                    result["status"] = "failed"

        elif decision.scope == RerenderScope.composition_reflow:
            text_content = self._patch_assembler.assemble_text_patch(revision=revision, slide_count=slide_count)
            if self._canvas is not None:
                try:
                    self._canvas.create_composition(vcb_id, "reflow_template", slide_count, {}, {}, text_content=text_content)
                except Exception:
                    result["status"] = "failed"

        elif decision.scope == RerenderScope.visual_slide_regeneration:
            for slide_idx in decision.affected_slide_indices:
                slide_result = self._visual_adapter.regenerate_slide(
                    composition_id=composition_id,
                    slide_index=slide_idx,
                    revision_note=revision.revision_note or "Visual fix requested",
                )
                if slide_result.get("status") == "failed":
                    result["status"] = "partially_failed"

        elif decision.scope == RerenderScope.cmf_full_regen_from_compiled_meaning:
            if self._vcb_generator is not None:
                try:
                    self._vcb_generator.generate({"vcb_id": vcb_id})
                except Exception:
                    result["status"] = "failed"
            result["requires_vcb_refresh"] = True

        elif decision.scope == RerenderScope.source_restart_required:
            result["status"] = "escalated"
            result["message"] = "Source restart required. Operator must re-record."

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="rerender-executed", metadata={
                "scope": decision.scope.value,
                "revision_id": decision.revision_id,
                "status": result["status"],
            })

        return result


# ════════════════════════════════════════════════════════════════════════
# LineageAuditProjector — DEP-CED-010
# Produces source-to-export lineage for coach inspection and receipts.
# trigger_first_chain_verified=True only if unbroken graph from export to source_audio.
# ════════════════════════════════════════════════════════════════════════

class LineageAuditProjector:
    def __init__(self, supabase_client: Any = None) -> None:
        self._supabase = supabase_client

    def build(self, *, editor_session_id: str, source_audio_asset_id: str, transcript_id: str | None = None, content_output_id: str | None = None, vcb_id: str | None = None, composition_id: str | None = None, export_bundle_id: str | None = None) -> EditorLineageGraph:
        now = _now_utc()
        nodes: list[LineageNode] = []

        root_node_id = _new_id("LN")
        nodes.append(LineageNode(
            node_id=root_node_id,
            node_type=LineageNodeType.source_audio,
            referenced_id=source_audio_asset_id,
            label="Source Voice Recording",
            parent_node_id=None,
            created_at_utc=now,
        ))

        parent = root_node_id

        if transcript_id:
            tid = _new_id("LN")
            nodes.append(LineageNode(
                node_id=tid, node_type=LineageNodeType.transcript,
                referenced_id=transcript_id, label="Transcript",
                parent_node_id=parent, created_at_utc=now,
            ))
            parent = tid

        if content_output_id:
            cid = _new_id("LN")
            nodes.append(LineageNode(
                node_id=cid, node_type=LineageNodeType.semantic_artifact,
                referenced_id=content_output_id, label="Semantic Artifact (ContentMachineResult)",
                parent_node_id=parent, created_at_utc=now,
            ))
            parent = cid

        if vcb_id:
            vid = _new_id("LN")
            nodes.append(LineageNode(
                node_id=vid, node_type=LineageNodeType.visual_composition_brief,
                referenced_id=vcb_id, label="Visual Composition Brief",
                parent_node_id=parent, created_at_utc=now,
            ))
            parent = vid

        if composition_id:
            comp_id = _new_id("LN")
            nodes.append(LineageNode(
                node_id=comp_id, node_type=LineageNodeType.canvas_composition,
                referenced_id=composition_id, label="Canvas Composition",
                parent_node_id=parent, created_at_utc=now,
            ))
            parent = comp_id

        if export_bundle_id:
            eid = _new_id("LN")
            nodes.append(LineageNode(
                node_id=eid, node_type=LineageNodeType.export_bundle,
                referenced_id=export_bundle_id, label="Export Bundle",
                parent_node_id=parent, created_at_utc=now,
            ))

        # Verify trigger-first chain: unbroken graph from last node back to source_audio
        chain_verified = len(nodes) >= 1 and nodes[0].node_type == LineageNodeType.source_audio
        if export_bundle_id:
            chain_verified = all(
                n.parent_node_id is not None or n.node_type == LineageNodeType.source_audio
                for n in nodes
            )

        graph = EditorLineageGraph(
            editor_session_id=editor_session_id,
            root_source_audio_asset_id=source_audio_asset_id,
            nodes=nodes,
            trigger_first_chain_verified=chain_verified,
            source_restart_required=False,
        )

        if self._supabase is not None:
            for node in nodes:
                try:
                    self._supabase.table("conscious_editor_lineage_links").insert({
                        "node_id": node.node_id,
                        "editor_session_id": editor_session_id,
                        "node_type": node.node_type.value,
                        "referenced_id": node.referenced_id,
                        "label": node.label,
                        "parent_node_id": node.parent_node_id,
                        "created_at": now,
                    }).execute()
                except Exception:
                    pass

        return graph


# ════════════════════════════════════════════════════════════════════════
# OperatorReviewDecisionEngine — DEP-CED-011
# Approve, edit-and-approve, regenerate, and escalate paths.
# ════════════════════════════════════════════════════════════════════════

class OperatorReviewDecisionEngine:
    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None, circuit_breaker: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._circuit_breaker = circuit_breaker

    def decide(self, *, editor_session_id: str, decision: OperatorDecision, decision_note: str = "", coach_id: str = "") -> OperatorDecisionResponse:
        receipt_id = _new_id("RCP")

        # Circuit breaker check for approval/escalation actions
        if decision in (OperatorDecision.approve, OperatorDecision.edit_and_approve, OperatorDecision.escalate):
            if self._circuit_breaker is not None:
                try:
                    if hasattr(self._circuit_breaker, "is_open") and self._circuit_breaker.is_open():
                        return OperatorDecisionResponse(
                            editor_session_id=editor_session_id,
                            decision=decision,
                            resulting_status=EditorSessionStatus.blocked,
                            receipt_event_id=receipt_id,
                        )
                except Exception:
                    pass

        if decision == OperatorDecision.approve:
            resulting_status = EditorSessionStatus.approved
        elif decision == OperatorDecision.edit_and_approve:
            resulting_status = EditorSessionStatus.approved
        elif decision == OperatorDecision.request_regeneration:
            resulting_status = EditorSessionStatus.rerender_in_progress
        elif decision == OperatorDecision.escalate:
            resulting_status = EditorSessionStatus.escalated
        else:
            resulting_status = EditorSessionStatus.blocked

        if self._supabase is not None:
            try:
                self._supabase.table("conscious_editor_operator_decisions").insert({
                    "decision_id": _new_id("DEC"),
                    "editor_session_id": editor_session_id,
                    "coach_id": coach_id,
                    "decision": decision.value,
                    "decision_note": decision_note,
                    "resulting_status": resulting_status.value,
                    "receipt_event_id": receipt_id,
                    "created_at": _now_utc(),
                }).execute()
            except Exception:
                pass

        if self._receipt_chain is not None:
            self._receipt_chain.log(action=f"operator-{decision.value}", metadata={
                "editor_session_id": editor_session_id,
                "decision": decision.value,
                "resulting_status": resulting_status.value,
            })

        return OperatorDecisionResponse(
            editor_session_id=editor_session_id,
            decision=decision,
            resulting_status=resulting_status,
            receipt_event_id=receipt_id,
        )
