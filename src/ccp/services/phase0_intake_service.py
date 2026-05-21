"""
FR-ERA3-33 Phase-0 Prospect Intake Service
===========================================
Business logic layer managing prospect records, attachments, readiness validation,
and receipt chain logging.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import hashlib

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.phase0_intake_models import (
    Phase0ProspectPacket,
    Phase0ProspectStatus,
    Phase0MediaSourceRef,
    Phase0TranscriptSourceRef,
    Phase0VoiceDnaSourceRef,
    Phase0VoiceCloneSourceRef,
    Phase0AvatarRef,
    Phase0TargetAudienceProfile,
    Phase0GuardianBusinessIntelligenceBundle,
    Phase0CaptionAttachment,
    Phase0AuditTargetDescriptor,
    Phase0MissingInputState,
    Phase0ProspectReadinessState,
    Phase0DeliveryReadiness
)


class Phase0IntakeService:
    """Manages the intake operations, validation, and serialization of prospect packets."""

    def __init__(self, default_coach_acronym: str = "P0A"):
        # In-memory persistence mirroring the production schema layout
        self.prospects: Dict[str, Phase0ProspectPacket] = {}
        self.default_coach_acronym = default_coach_acronym

        # Active transaction ledger
        self.ledger: List[Dict[str, Any]] = []

    def _get_acronym(self, packet: Phase0ProspectPacket) -> str:
        """Extract a 3-letter acronym from packet or default."""
        if packet.coach_id and len(packet.coach_id) >= 3:
            return packet.coach_id[:3].upper()
        return self.default_coach_acronym.upper()

    def create_prospect(
        self,
        prospect_id: str,
        display_name: str,
        coach_id: Optional[str] = None,
        campaign_metadata: Optional[Dict[str, Any]] = None
    ) -> Phase0ProspectPacket:
        """Creates a fresh prospect draft packet."""
        if not prospect_id or not prospect_id.strip():
            raise ValueError("Prospect ID must be non-empty")
        if not display_name or not display_name.strip():
            raise ValueError("Display name must be non-empty")

        packet = Phase0ProspectPacket(
            prospect_id=prospect_id,
            display_name=display_name,
            coach_id=coach_id,
            status=Phase0ProspectStatus.DRAFT,
            campaign_metadata=campaign_metadata or {}
        )

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-PROSPECT-CREATE",
            asset_id=packet.packet_id,
            person_id=prospect_id,
            input_summary=f"Create prospect draft for '{display_name}'",
            output_summary=f"Draft packet created with ID: {packet.packet_id}",
            decision="approved",
            metadata={"campaign": packet.campaign_metadata}
        )

        packet.receipt_chain_refs.append(entry.receipt_id)
        self.prospects[prospect_id] = packet
        return packet

    def get_prospect(self, prospect_id: str) -> Optional[Phase0ProspectPacket]:
        """Retrieves a prospect packet by ID."""
        return self.prospects.get(prospect_id)

    def attach_media(
        self,
        prospect_id: str,
        media_kind: str,
        storage_uri: str,
        original_filename: str,
        file_size_bytes: int,
        mime_type: Optional[str] = None,
        duration_seconds: Optional[float] = None,
        image_width: Optional[int] = None,
        image_height: Optional[int] = None,
        checksum_sha256: Optional[str] = None,
    ) -> Phase0MediaSourceRef:
        """Attaches a media source ref to a prospect record."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        if not checksum_sha256:
            content_str = f"{prospect_id}:{original_filename}:{file_size_bytes}"
            checksum_sha256 = hashlib.sha256(content_str.encode()).hexdigest()

        # Log upload transaction
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-MEDIA-UPLOAD",
            person_id=prospect_id,
            input_summary=f"Register media: {original_filename} ({media_kind})",
            output_summary=f"URI: {storage_uri}",
            decision="approved",
            metadata={
                "size_bytes": file_size_bytes,
                "mime_type": mime_type,
                "duration": duration_seconds
            }
        )

        ref = Phase0MediaSourceRef(
            prospect_id=prospect_id,
            coach_id=packet.coach_id,
            media_kind=media_kind,
            storage_uri=storage_uri,
            original_filename=original_filename,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            duration_seconds=duration_seconds,
            image_width=image_width,
            image_height=image_height,
            checksum_sha256=checksum_sha256,
            upload_receipt_id=entry.receipt_id
        )

        packet.media_sources.append(ref)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.status = Phase0ProspectStatus.COLLECTING_INPUTS
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return ref

    def attach_transcript(
        self,
        prospect_id: str,
        source_kind: str,
        raw_text: Optional[str] = None,
        storage_uri: Optional[str] = None,
        linked_media_source_id: Optional[str] = None,
        language_hint: Optional[str] = "en"
    ) -> Phase0TranscriptSourceRef:
        """Attaches transcript context to the prospect packet."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        word_count = len(raw_text.split()) if raw_text else 0

        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-TRANSCRIPT-ATTACH",
            person_id=prospect_id,
            input_summary=f"Attach transcript: {source_kind}",
            output_summary=f"Words: {word_count}",
            decision="approved",
            metadata={"language": language_hint, "linked_media": linked_media_source_id}
        )

        ref = Phase0TranscriptSourceRef(
            prospect_id=prospect_id,
            source_kind=source_kind,
            linked_media_source_id=linked_media_source_id,
            storage_uri=storage_uri,
            raw_text=raw_text,
            language_hint=language_hint,
            word_count=word_count
        )

        packet.transcript_sources.append(ref)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return ref

    def attach_voice_dna(
        self,
        prospect_id: str,
        linked_media_source_ids: List[str],
        notes: Optional[str] = None,
        quality_confidence: float = 1.0
    ) -> Phase0VoiceDnaSourceRef:
        """Attaches a Voice DNA reference to the prospect packet."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-VOICEDNA-ATTACH",
            person_id=prospect_id,
            input_summary="Attach Voice DNA reference",
            output_summary=f"Confidence: {quality_confidence}",
            decision="approved",
            metadata={"linked_sources": linked_media_source_ids, "notes": notes}
        )

        ref = Phase0VoiceDnaSourceRef(
            prospect_id=prospect_id,
            linked_media_source_ids=linked_media_source_ids,
            notes=notes,
            quality_confidence=quality_confidence
        )

        packet.voice_dna_sources.append(ref)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return ref

    def attach_voice_clone(
        self,
        prospect_id: str,
        linked_media_source_ids: List[str],
        duration_seconds_total: float,
        quality_confidence: float = 1.0,
        consent_status: Optional[str] = "granted"
    ) -> Phase0VoiceCloneSourceRef:
        """Attaches a Voice Clone reference to the prospect packet."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-VOICECLON-ATTACH",
            person_id=prospect_id,
            input_summary="Attach Voice Clone parameters",
            output_summary=f"Duration: {duration_seconds_total}s",
            decision="approved",
            metadata={"consent": consent_status, "confidence": quality_confidence}
        )

        ref = Phase0VoiceCloneSourceRef(
            prospect_id=prospect_id,
            linked_media_source_ids=linked_media_source_ids,
            duration_seconds_total=duration_seconds_total,
            quality_confidence=quality_confidence,
            consent_status=consent_status
        )

        packet.voice_clone_sources.append(ref)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return ref

    def attach_avatar(
        self,
        prospect_id: str,
        image_source_ids: List[str],
        style_notes: Optional[str] = None,
        pose_notes: Optional[str] = None,
        quality_confidence: float = 1.0
    ) -> Phase0AvatarRef:
        """Attaches Avatar reference criteria."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-AVATAR-ATTACH",
            person_id=prospect_id,
            input_summary="Attach Avatar branding criteria",
            output_summary=f"Images: {len(image_source_ids)}",
            decision="approved",
            metadata={"style": style_notes, "pose": pose_notes}
        )

        ref = Phase0AvatarRef(
            prospect_id=prospect_id,
            image_source_ids=image_source_ids,
            style_notes=style_notes,
            pose_notes=pose_notes,
            quality_confidence=quality_confidence
        )

        packet.avatar_refs.append(ref)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return ref

    def set_audience_profile(
        self,
        prospect_id: str,
        primary_audience_label: str,
        pain_points: List[str],
        desires: List[str],
        market_context: Optional[str] = None,
        offer_context: Optional[str] = None,
        tone_notes: Optional[str] = None,
        language_notes: Optional[str] = None
    ) -> Phase0TargetAudienceProfile:
        """Sets the target audience profile context."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-AUDIENCE-PROFILE-ATTACH",
            person_id=prospect_id,
            input_summary=f"Set audience context: {primary_audience_label}",
            output_summary="Profile attached",
            decision="approved",
            metadata={"pain_points": len(pain_points), "desires": len(desires)}
        )

        profile = Phase0TargetAudienceProfile(
            prospect_id=prospect_id,
            primary_audience_label=primary_audience_label,
            pain_points=pain_points,
            desires=desires,
            market_context=market_context,
            offer_context=offer_context,
            tone_notes=tone_notes,
            language_notes=language_notes
        )

        packet.target_audience_profile = profile
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return profile

    def attach_guardian_bi(
        self,
        prospect_id: str,
        market_summary: str,
        offer_summary: str,
        positioning_notes: Optional[str] = None,
        objections: List[str] = None,
        differentiation_notes: Optional[str] = None,
        proof_notes: Optional[str] = None,
        raw_artifact_refs: Optional[Dict[str, Any]] = None
    ) -> Phase0GuardianBusinessIntelligenceBundle:
        """Attaches business intelligence bundle gathered from the outreach target."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-GUARDIAN-BI-ATTACH",
            person_id=prospect_id,
            input_summary="Attach Guardian Outreach Business Intelligence",
            output_summary="Bundle attached",
            decision="approved",
            metadata={"objections": len(objections or [])}
        )

        bundle = Phase0GuardianBusinessIntelligenceBundle(
            prospect_id=prospect_id,
            market_summary=market_summary,
            offer_summary=offer_summary,
            positioning_notes=positioning_notes,
            objections=objections or [],
            differentiation_notes=differentiation_notes,
            proof_notes=proof_notes,
            raw_artifact_refs=raw_artifact_refs or {}
        )

        packet.guardian_business_intelligence_bundle = bundle
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return bundle

    def create_audit_target(
        self,
        prospect_id: str,
        content_type: str,
        primary_media_source_ids: Optional[List[str]] = None,
        platform_hint: Optional[str] = "instagram",
        content_url: Optional[str] = None,
        archetype_hint: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Phase0AuditTargetDescriptor:
        """Creates an audit target mapping."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-AUDIT-TARGET-ATTACH",
            person_id=prospect_id,
            input_summary=f"Create audit target ({content_type})",
            output_summary="Audit target registered",
            decision="approved",
            metadata={"platform": platform_hint, "url": content_url}
        )

        descriptor = Phase0AuditTargetDescriptor(
            prospect_id=prospect_id,
            content_type=content_type,
            primary_media_source_ids=primary_media_source_ids or [],
            platform_hint=platform_hint,
            content_url=content_url,
            archetype_hint=archetype_hint,
            notes=notes
        )

        packet.audit_targets.append(descriptor)
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return descriptor

    def attach_caption(
        self,
        prospect_id: str,
        audit_target_id: str,
        caption_text: str,
        source_kind: str,
        language_hint: Optional[str] = "en"
    ) -> Phase0CaptionAttachment:
        """Attaches caption text reference for a designated audit target."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        target = next((t for t in packet.audit_targets if t.audit_target_id == audit_target_id), None)
        if not target:
            raise ValueError(f"Audit Target Descriptor with ID {audit_target_id} not found")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-CAPTION-ATTACH",
            person_id=prospect_id,
            input_summary=f"Attach caption copy ({source_kind})",
            output_summary=f"Attached to: {audit_target_id}",
            decision="approved",
            metadata={"char_count": len(caption_text)}
        )

        attachment = Phase0CaptionAttachment(
            prospect_id=prospect_id,
            audit_target_id=audit_target_id,
            caption_text=caption_text,
            source_kind=source_kind,
            language_hint=language_hint
        )

        packet.captions.append(attachment)
        target.caption_id = attachment.caption_id
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return attachment

    def validate_readiness(self, prospect_id: str) -> Phase0ProspectReadinessState:
        """Runs the Rule-based quality gates checking for missing input boundaries."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        acronym = self._get_acronym(packet)
        blocking_inputs: List[Phase0MissingInputState] = []
        warning_inputs: List[Phase0MissingInputState] = []

        # ── 1. Check Source Materials (Interview Video/Audio or Transcript Text) ──
        has_media = len(packet.media_sources) > 0
        has_transcript = any(t.raw_text and len(t.raw_text.strip()) > 0 for t in packet.transcript_sources)
        
        if not has_media and not has_transcript:
            blocking_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_interview_material",
                    severity="blocking",
                    message="No interview voice media or transcription files were provided.",
                    resolution_hint="Upload at least one .mp3/.m4a/.wav recording or paste raw translatable text."
                )
            )

        # ── 2. Check Audit Target ──
        if len(packet.audit_targets) == 0:
            blocking_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_audit_target",
                    severity="blocking",
                    message="At least one baseline audit target (single image post, carousel post, reel video) is required.",
                    resolution_hint="Register an audit target mapping to baseline content for diagnosis."
                )
            )

        # ── 3. Check Caption / Copy for attached Audit Targets ──
        for t in packet.audit_targets:
            caption_exists = any(c.audit_target_id == t.audit_target_id for c in packet.captions)
            if not caption_exists:
                warning_inputs.append(
                    Phase0MissingInputState(
                        prospect_id=prospect_id,
                        missing_code="missing_caption_attachment",
                        severity="warning",
                        message=f"Audit target {t.audit_target_id} has no matching caption block.",
                        resolution_hint="Attach the corresponding caption copywriting for precise anti-slop assessment."
                    )
                )

        # ── 4. Target Audience Profile Check ──
        if not packet.target_audience_profile:
            warning_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_target_audience",
                    severity="warning",
                    message="No target audience profile is attached to this workspace.",
                    resolution_hint="Provide target audience context, pain points, and desires."
                )
            )

        # ── 5. Guardian Outreach intelligence Check ──
        if not packet.guardian_business_intelligence_bundle:
            warning_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_guardian_bi",
                    severity="warning",
                    message="Outreach target objections and market positioning notes from Guardian are absent.",
                    resolution_hint="Run Guardian business intelligence collection or fill in outline notes manually."
                )
            )

        # ── 6. Voice DNA / Clone Checks ──
        if len(packet.voice_dna_sources) == 0 and len(packet.voice_clone_sources) == 0:
            warning_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_voice_source",
                    severity="warning",
                    message="No voice parameters (clone profiles or DNA metrics) are available to match voice profiles.",
                    resolution_hint="Register a voice DNA parameter set to avoid generic model slop."
                )
            )

        # ── 7. Avatar Image Checklist ──
        if len(packet.avatar_refs) == 0:
            warning_inputs.append(
                Phase0MissingInputState(
                    prospect_id=prospect_id,
                    missing_code="missing_avatar_reference",
                    severity="warning",
                    message="No facial branding portrait photos or avatar references were provided.",
                    resolution_hint="Supply a 2D avatar reference image to enable visually consistent proof assets."
                )
            )

        # ── Calculate status and delivery readiness ──
        if len(blocking_inputs) > 0:
            status = Phase0ProspectStatus.BLOCKED_MISSING_INPUTS
            readiness = Phase0DeliveryReadiness.NOT_READY
            summary = f"Blocked by {len(blocking_inputs)} missing input(s)."
        elif len(warning_inputs) > 0:
            status = Phase0ProspectStatus.AWAITING_VALIDATION
            readiness = Phase0DeliveryReadiness.CONDITIONALLY_READY
            summary = f"Structurally valid, but needs review on {len(warning_inputs)} warnings."
        else:
            status = Phase0ProspectStatus.READY_FOR_PHASE0
            readiness = Phase0DeliveryReadiness.READY
            summary = "All inputs gathered and fully validated."

        # Write verification receipt
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-READINESS-VALIDATE",
            person_id=prospect_id,
            input_summary="Evaluate Phase-0 workspace completeness gates",
            output_summary=f"Readiness: {readiness.value} | Status: {status.value}",
            decision="approved",
            metadata={
                "blocking_count": len(blocking_inputs),
                "warning_count": len(warning_inputs)
            }
        )

        readiness_state = Phase0ProspectReadinessState(
            prospect_id=prospect_id,
            packet_status=status,
            delivery_readiness=readiness,
            blocking_missing_inputs=blocking_inputs,
            warning_missing_inputs=warning_inputs,
            readiness_summary=summary,
            validation_receipt_id=entry.receipt_id
        )

        packet.missing_input_states = blocking_inputs + warning_inputs
        packet.readiness_state = readiness_state
        packet.status = status
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return readiness_state

    def emit_handoff_packet(self, prospect_id: str) -> Phase0ProspectPacket:
        """Emits an immutable frozen snapshot for the Phase-0 production runtime."""
        packet = self.get_prospect(prospect_id)
        if not packet:
            raise ValueError(f"Prospect with ID {prospect_id} not found")

        # Must run validation to ensure status is up to date
        self.validate_readiness(prospect_id)

        if packet.status == Phase0ProspectStatus.BLOCKED_MISSING_INPUTS:
            raise ValueError("Cannot handoff a blocked packet with unresolved blocking constraints")

        acronym = self._get_acronym(packet)
        rc = ReceiptChain(coach_acronym=acronym)
        entry = rc.log(
            agent_id="phase0_intake_service",
            action="PHASE0-PACKET-EMIT",
            asset_id=packet.packet_id,
            person_id=prospect_id,
            input_summary=f"Emit handoff packet for prospect '{packet.display_name}'",
            output_summary=f"Transitioned status to: handed_off",
            decision="approved",
            metadata={"status": packet.status}
        )

        packet.status = Phase0ProspectStatus.HANDED_OFF
        packet.receipt_chain_refs.append(entry.receipt_id)
        packet.updated_at = datetime.now(timezone.utc).isoformat()
        return packet
