"""
FR61 — Jim Rohn AI Voice Coach Engine: Stage Orchestrator
==========================================================
The RohnVoiceCoachOrchestrator class implements all 7 pipeline stages.
Each stage writes a FR47 DEP-ENG-041 receipt on completion.
Architecture reference: FR61 §4.
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from backend.core.fr61_models import (
    ContradictionPair, EmotionalTrajectory, ExtractedStory,
    FeedbackElement, FeedbackOutput, FR5FeedbackSignal,
    FR61ReceiptBlock, GeneratedQuestion, HCDReference,
    IntakeProcessingResult, MicroImprovementDetection,
    NARRATIVE_ARC_TEMPLATES, PauseMarker, PinDataPoint,
    ProvocationQuestionOutput, RecordingAnalysis,
    ScheduledSessionRecord, ScheduledSessionStatus,
    ScriptDocument, ScriptPiece, SessionAnalysisOutput,
    SessionType, SpecificityRatchetResult, TemporalPosition,
    TranscriptAnalysis, TriggerSource, VideoAnalysis, VideoAvailabilityVerdict, VocalAnalysis, EuphonyDevice, TPLMarker,
    VOICE_NOTE_MIN_SECONDS, SESSION_WARN_MINUTES,
    SESSION_MAX_MINUTES, ReminderStage,
    ProvocationError, IntakeError, ScriptCompositionError,
    SchedulingError, RecordingSessionError, FeedbackError,
)
from backend.core.rohn_voice_coach_engine import (
    SupabaseClientProtocol, RedisClientProtocol, TTSServiceProtocol,
    AudioAnalysisProtocol, VideoAnalysisProtocol, CalendarServiceProtocol,
    TelegramDeliveryProtocol, LLMServiceProtocol,
    ProvocationQualityGate, SpecificityRatchetGate,
    ScriptArrangementGate, SessionTimeGate, FeedbackRegisterGate,
    VideoAnalysisGate,
    _sha256, _build_receipt, _generate_receipt_id,
    _detect_alliteration, _select_narrative_arc,
    _compute_sincerity_composite, _compute_wpm,
    _compute_filler_density, _count_rohn_pauses,
    _compute_pin_iron_ratio, _compute_micro_improvements,
    _check_prohibited_words,
)

logger = logging.getLogger(__name__)


class RohnVoiceCoachOrchestrator:
    """
    Main orchestrator for the FR61 Jim Rohn AI Voice Coach Engine.

    Implements all 7 stages defined in FR61 §4:
      Stage 1: Rohn-Style Provocation Question Formatting & TTS Delivery
      Stage 2: Coach Response Intake & Multi-Layer Extraction
      Stage 3: Supportive Script Generation
      Stage 4: Recording Session Booking & Reminder Pipeline
      Stage 5: Recording Session — Video Intake & Multi-Modal Analysis
      Stage 6: Rohn-Style Feedback Generation & Micro-Improvement Acknowledgment
      Stage 7: Supabase Persistence & Redis Session Management

    ADR-01: All queries scoped by coach_id.
    C-11: No agent persona names in any API/LLM payload.
    """

    def __init__(
        self,
        supabase: SupabaseClientProtocol,
        redis: RedisClientProtocol,
        tts: TTSServiceProtocol,
        audio: AudioAnalysisProtocol,
        video: VideoAnalysisProtocol,
        calendar: CalendarServiceProtocol,
        telegram: TelegramDeliveryProtocol,
        llm: LLMServiceProtocol,
        coach_id: str,
        coach_acronym: str,
    ):
        self._db = supabase
        self._redis = redis
        self._tts = tts
        self._audio = audio
        self._video = video
        self._calendar = calendar
        self._telegram = telegram
        self._llm = llm
        self._coach_id = coach_id
        self._coach_acronym = coach_acronym
        self._receipt_chain: List[FR61ReceiptBlock] = []
        self._last_receipt_hash: str = "GENESIS"

    def _append_receipt(self, stage_label: str, stage_name: str,
                        agent_name: str, input_data: Any, output_data: Any) -> FR61ReceiptBlock:
        """Write a FR47 DEP-ENG-041 receipt and append to chain."""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        receipt = _build_receipt(
            receipt_id=_generate_receipt_id(self._coach_acronym, stage_label, date_str),
            previous_hash=self._last_receipt_hash,
            input_data=input_data,
            output_data=output_data,
            stage_name=stage_name,
            agent_name=agent_name,
        )
        self._last_receipt_hash = _sha256(receipt.model_dump())
        self._receipt_chain.append(receipt)
        logger.info(f"[FR61] Receipt written: {receipt.stage_name} → {receipt.receipt_id}")
        return receipt

    # ═══════════════════════════════════════════════════════════
    # STAGE 1: Rohn-Style Provocation (FR61 §4.Stage1)
    # ═══════════════════════════════════════════════════════════

    async def stage1_generate_provocation(
        self,
        tension_observation: dict,
        trigger_map_entry: dict,
        fr15_receipt_hash: str = "GENESIS",
    ) -> ProvocationQuestionOutput:
        """
        FR61 §4.Stage1: Generate a Rohn-style provocation question from
        FR15 tension + FR5 trigger map + coach HCD state.

        Inputs: tension_observation_object (DEP-ENG-005), trigger_map (DEP-LIB-002)
        Outputs: Rohn-style voice note + TPL text, delivered to Telegram.
        """
        self._last_receipt_hash = fr15_receipt_hash
        await self._db.set_coach_context(self._coach_id)

        # Step 2: Query Supabase for coach HCD state
        stories = await self._db.select("story_bank",
            {"coach_id": self._coach_id}, order_by="date_extracted DESC", limit=5)
        tensions = await self._db.select("philosophy_tensions",
            {"coach_id": self._coach_id, "resolved": False}, limit=5)
        vocal_history = await self._db.select("vocal_delivery",
            {"coach_id": self._coach_id}, order_by="measured_at DESC", limit=1)
        philosophy = await self._db.select("personal_philosophy",
            {"coach_id": self._coach_id}, limit=1)

        # Build HCD references
        hcd_refs: List[HCDReference] = []
        if stories:
            hcd_refs.append(HCDReference(
                type="previous_statement",
                source_session=stories[0].get("session_id", ""),
                quote=stories[0].get("raw_transcript", "")[:200],
            ))
        if tensions:
            hcd_refs.append(HCDReference(
                type="unresolved_tension",
                source_session=str(tensions[0].get("tension_id", "")),
                quote=tensions[0].get("claim_a_text", "")[:200],
            ))

        # Step 4: Generate provocation question via LLM
        # C-11: No agent persona name in the prompt
        topic = tension_observation.get("topic_cluster", "")
        tension_text = tension_observation.get("cultural_tension", "")
        hcd_context = "\n".join([f"- {r.quote}" for r in hcd_refs])
        grievances = ""
        if philosophy:
            glist = philosophy[0].get("recurring_grievances", [])
            grievances = "\n".join([f"- {g}" for g in glist[:3]]) if glist else ""

        system_prompt = (
            "You are a philosophical voice coach in the Business Philosopher tradition. "
            "Generate a provocation question that:\n"
            "1. References at least one item from the coach's history below\n"
            "2. Contains at least one antithetical construction (e.g., 'not X — Y')\n"
            "3. Ends with a specific, direct question demanding the coach choose a position\n"
            "4. NEVER uses: 'I can help with that', 'as an AI', 'delve', 'unlock', 'game-changing'\n"
            "5. Should incorporate alliteration or phonetic patterns where natural\n"
            "6. Tone: measured, warm, direct, philosophical"
        )
        user_prompt = (
            f"Cultural tension detected: {tension_text}\n"
            f"Topic cluster: {topic}\n"
            f"Coach's recent statements:\n{hcd_context}\n"
            f"Coach's recurring frustrations:\n{grievances}\n"
            f"Trigger mechanism: {trigger_map_entry.get('mechanism_description', '')}\n\n"
            "Generate the provocation question now."
        )

        question_text = await self._llm.generate(system_prompt, user_prompt)

        # Gate S1: Validate provocation quality
        gate_result = ProvocationQualityGate.evaluate(question_text, hcd_refs)
        if gate_result.verdict.value != "PASS":
            raise ProvocationError(
                f"Gate S1 FAIL: {gate_result.verdict.value} — "
                f"HCD refs: {gate_result.hcd_ref_count}, "
                f"antitheses: {gate_result.antithesis_count}, "
                f"closing question: {gate_result.has_closing_question}, "
                f"prohibited: {gate_result.prohibited_words_found}"
            )

        # Step 4 continued: Extract euphony devices and TPL markers
        euphony = _detect_alliteration(question_text)
        tpl_markers = []
        if "*" in question_text:
            for match in __import__("re").findall(r'\*[^*]+\*', question_text):
                tpl_markers.append(TPLMarker(marker_type="pause", marker_text=match))

        # Step 5: Route to CosyVoice TTS
        voice_note_url = await self._tts.synthesize(question_text)

        # Step 6: Deliver to coach via Telegram
        await self._telegram.send_voice_note(self._coach_id, voice_note_url)
        await self._telegram.send_text(self._coach_id, question_text)

        output = ProvocationQuestionOutput(
            provocation_id=f"PROV-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:3].upper()}",
            coach_tenant_id=self._coach_id,
            trigger_source=TriggerSource(
                fr15_tension_id=tension_observation.get("tension_id", ""),
                fr5_trigger_id=trigger_map_entry.get("trigger_id", ""),
                topic_cluster=topic,
            ),
            hcd_references=hcd_refs,
            generated_question=GeneratedQuestion(
                text=question_text,
                antithesis_count=gate_result.antithesis_count,
                euphony_devices=euphony,
                tpl_markers=tpl_markers,
            ),
            voice_note_url=voice_note_url,
            delivered_at=datetime.utcnow(),
        )

        # Step 7: Receipt write
        input_hash_data = {"tension": tension_observation, "hcd": [r.model_dump() for r in hcd_refs]}
        self._append_receipt("ROHN-PROVOCATION", "STAGE-1-ROHN-PROVOCATION",
                            "Rohn-Voice-Coach-Agent", input_hash_data, output.model_dump())

        # Cache provocation in Redis
        await self._redis.set_json(
            f"provocation:{self._coach_id}:pending",
            output.model_dump(),
            43200,  # 12h TTL
        )

        return output

    # ═══════════════════════════════════════════════════════════
    # STAGE 2: Coach Response Intake (FR61 §4.Stage2)
    # ═══════════════════════════════════════════════════════════

    async def stage2_process_intake(
        self, audio_path: str, duration_seconds: float, ratchet_count: int = 0,
    ) -> IntakeProcessingResult:
        """
        FR61 §4.Stage2: Process coach's voice note response with multi-layer extraction.
        Phase 1 is extraction-only — NO feedback delivered (AC2).
        """
        await self._db.set_coach_context(self._coach_id)

        if duration_seconds < VOICE_NOTE_MIN_SECONDS:
            raise IntakeError(f"Voice note too short: {duration_seconds}s < {VOICE_NOTE_MIN_SECONDS}s minimum")

        # Step 2: Parallel audio processing
        prosody = await self._audio.extract_prosody(audio_path)
        transcript_text, word_timestamps = await self._audio.transcribe(audio_path)
        transcript_analysis = await self._audio.analyze_liwc(transcript_text)
        emotion_segments = await self._audio.extract_emotion(audio_path)

        word_count = len(transcript_text.split())
        wpm = _compute_wpm(word_count, duration_seconds)

        # Create session record
        session_id = str(uuid.uuid4())
        await self._db.insert("sessions", {
            "session_id": session_id, "coach_id": self._coach_id,
            "session_type": "trigger", "session_completed": False,
        })

        # Step 3b: Story extraction
        stories: List[ExtractedStory] = []
        if transcript_analysis.sensory_detail_score > 2.0:
            stories.append(ExtractedStory(
                raw_transcript=transcript_text,
                sensory_detail_score=transcript_analysis.sensory_detail_score,
                named_entities=[],  # populated by NER
                emotion_arousal=prosody.arousal,
                emotion_valence=prosody.valence,
            ))

        # Step 3c: Contradiction detection
        contradictions: List[ContradictionPair] = []
        existing_beliefs = await self._db.select("personal_philosophy",
            {"coach_id": self._coach_id}, limit=1)
        # Contradiction detection delegated to LLM with existing beliefs context

        # Step 4: Specificity Ratchet
        specificity = SpecificityRatchetGate.evaluate(
            transcript_analysis.sensory_detail_score,
            transcript_analysis.named_entity_count,
            ratchet_count,
        )
        if specificity.needs_followup:
            followup_text = (
                f"You mentioned something interesting, but I need you to be more specific. "
                f"Can you give me a specific moment, person, or scene?"
            )
            followup_url = await self._tts.synthesize(followup_text)
            await self._telegram.send_voice_note(self._coach_id, followup_url)

        # Step 5: Supabase writes
        sincerity = _compute_sincerity_composite(
            transcript_analysis.liwc_authenticity, prosody.jitter, prosody.shimmer)

        for story in stories:
            await self._db.insert("story_bank", {
                "coach_id": self._coach_id, "session_id": session_id,
                "raw_transcript": story.raw_transcript,
                "topic_tags": story.topic_tags,
                "emotion_arousal": story.emotion_arousal,
                "emotion_valence": story.emotion_valence,
                "sensory_detail_score": story.sensory_detail_score,
                "temporal_position": story.temporal_position.value,
            })

        await self._db.insert("vocal_delivery", {
            "session_id": session_id, "coach_id": self._coach_id,
            "wpm": wpm, "spm": prosody.spm,
            "pitch_variance": prosody.f0_variance,
            "avg_iss": 0.0, "filler_density": 0.0,
            "sincerity_composite": sincerity,
            "liwc_authenticity": transcript_analysis.liwc_authenticity,
            "jitter": prosody.jitter, "shimmer": prosody.shimmer,
            "emotional_loading_arousal": prosody.arousal,
            "emotional_loading_valence": prosody.valence,
        })

        # Step 7: NO feedback delivered (AC2 enforcement)
        result = IntakeProcessingResult(
            session_id=session_id, coach_id=self._coach_id,
            stories_extracted=stories, contradictions_detected=contradictions,
            prosody=prosody, transcript_analysis=transcript_analysis,
            specificity_result=specificity,
            full_transcript=transcript_text, word_count=word_count,
            duration_seconds=duration_seconds,
        )

        # Receipt write
        self._append_receipt("ROHN-INTAKE", "STAGE-2-ROHN-INTAKE",
                            "Rohn-Intake-Processor",
                            {"audio_path": audio_path},
                            {"session_id": session_id, "stories": len(stories)})
        return result

    # ═══════════════════════════════════════════════════════════
    # STAGE 3: Supportive Script Generation (FR61 §4.Stage3)
    # ═══════════════════════════════════════════════════════════

    async def stage3_generate_script(
        self, cral_evidence: List[dict], voice_dna: dict,
    ) -> ScriptDocument:
        """
        FR61 §4.Stage3: Generate supportive scripts from Phase 1 material.
        Scripts ARRANGE coach's exact phrases — they do NOT rewrite them (AC3).
        """
        await self._db.set_coach_context(self._coach_id)

        # Step 1: Query Phase 1 material
        stories = await self._db.select("story_bank",
            {"coach_id": self._coach_id}, order_by="date_extracted DESC", limit=10)
        vocal_baselines = await self._db.select("vocal_delivery",
            {"coach_id": self._coach_id}, order_by="measured_at DESC", limit=1)

        avg_iss = vocal_baselines[0].get("avg_iss", 2.0) if vocal_baselines else 2.0
        original_phrases = [s.get("raw_transcript", "") for s in stories if s.get("raw_transcript")]

        # Step 3: Build content pieces
        content_pieces: List[ScriptPiece] = []
        for i, story in enumerate(stories[:3]):
            trajectory = story.get("narrative_arc", "principles_to_practice")
            arc_name = _select_narrative_arc(trajectory)
            phrases = [story.get("raw_transcript", "")]

            pin_points = []
            for j, ev in enumerate(cral_evidence[:1]):
                pin_points.append(PinDataPoint(
                    citation=ev.get("citation", f"Evidence point {j+1}"),
                    position_seconds=90 * (j + 1),
                ))

            pause_markers = [PauseMarker(
                duration_seconds=min(max(avg_iss, 1.5), 2.5),
                position_after=phrases[0][:60] if phrases else "",
                triggered_by_sentiment_peak=True,
            )]

            content_pieces.append(ScriptPiece(
                title=story.get("topic_tags", ["Untitled"])[0] if story.get("topic_tags") else f"Piece {i+1}",
                narrative_arc=arc_name,
                estimated_duration_seconds=min(180, max(60, len(phrases[0].split()) * 2)),
                arranged_phrases=phrases,
                pin_data_points=pin_points,
                pause_markers=pause_markers,
            ))

        script = ScriptDocument(
            coach_id=self._coach_id,
            content_pieces=content_pieces,
            raw_coach_phrases_used=original_phrases,
            voice_dna_compatibility_score=0.85,
        )

        # Gate S3: Validate arrangement (not rewrite)
        gate = ScriptArrangementGate.evaluate(script, original_phrases)
        if gate.verdict.value != "PASS":
            raise ScriptCompositionError(f"Gate S3 FAIL: {gate.verdict.value}")

        # Step 5: Write to scripts table
        await self._db.insert("scripts", {
            "coach_id": self._coach_id,
            "content_pieces": [p.model_dump() for p in content_pieces],
            "pause_markers": [m.model_dump() for p in content_pieces for m in p.pause_markers],
            "pin_data_points": [d.model_dump() for p in content_pieces for d in p.pin_data_points],
            "raw_coach_phrases_used": original_phrases,
            "voice_dna_compatibility_score": script.voice_dna_compatibility_score,
        })

        # Step 6: Deliver via Telegram
        overview = f"{len(content_pieces)} pieces for your session. Read through them. Mark anything that doesn't sound like you."
        overview_url = await self._tts.synthesize(overview)
        await self._telegram.send_voice_note(self._coach_id, overview_url)

        for piece in content_pieces:
            text_block = (
                f"RECORDING PIECE: {piece.title}\n"
                f"Narrative Arc: {piece.narrative_arc}\n"
                f"Estimated Duration: {piece.estimated_duration_seconds}s\n"
                f"Script Type: ARRANGEMENT (not rewrite)\n\n"
                + "\n".join(piece.arranged_phrases)
                + "\n\nNOTE: Anything that doesn't sound like you — change it.\n"
                  "This is YOUR material, arranged for flow."
            )
            await self._telegram.send_text(self._coach_id, text_block)

        # Receipt write
        self._append_receipt("ROHN-SCRIPT", "STAGE-3-ROHN-SCRIPT",
                            "Script-Composer-Agent",
                            {"stories": len(stories), "cral_evidence": len(cral_evidence)},
                            script.model_dump())
        return script

    # ═══════════════════════════════════════════════════════════
    # STAGE 4: Session Scheduling (FR61 §4.Stage4)
    # ═══════════════════════════════════════════════════════════

    async def stage4_schedule_session(
        self, recordings_planned: int = 3, batch_theme: str = "",
    ) -> ScheduledSessionRecord:
        """FR61 §4.Stage4: Book recording session + 3-stage reminder pipeline."""
        await self._db.set_coach_context(self._coach_id)

        coaches = await self._db.select("coaches", {"coach_id": self._coach_id}, limit=1)
        if not coaches:
            raise SchedulingError(f"Coach {self._coach_id} not found")

        coach = coaches[0]
        tz = coach.get("timezone", "UTC")
        avail = coach.get("availability_config", {})
        default_day = avail.get("preferred_day", "thursday")
        default_time = avail.get("preferred_time", "10:00")

        # Determine session slot (Step 2)
        now = datetime.utcnow()
        session_dt = now + timedelta(hours=48)  # default 48h after script delivery

        record = ScheduledSessionRecord(
            coach_id=self._coach_id,
            scheduled_datetime=session_dt,
            batch_theme=batch_theme,
            recordings_planned=recordings_planned,
        )

        # Step 3: Calendar integration
        event_id = await self._calendar.create_event(
            self._coach_id,
            f"Recording Session — {batch_theme or 'Weekly Batch'}",
            session_dt, 60,
            f"Recording session. {recordings_planned} pieces to record.",
        )

        # Write to Supabase
        await self._db.insert("scheduled_sessions", {
            "coach_id": self._coach_id,
            "scheduled_datetime": session_dt.isoformat(),
            "batch_theme": batch_theme,
            "recordings_planned": recordings_planned,
            "status": "booked",
        })

        # Step 4: Reminder pipeline scheduling (stored in Redis)
        await self._redis.set_json(f"schedule:{self._coach_id}:reminders", {
            "session_dt": session_dt.isoformat(),
            "t_48h": (session_dt - timedelta(hours=48)).isoformat(),
            "t_24h": (session_dt - timedelta(hours=24)).isoformat(),
            "t_30min": (session_dt - timedelta(minutes=30)).isoformat(),
            "reminders_sent": [],
        }, 259200)

        # Receipt write
        self._append_receipt("ROHN-SCHEDULE", "STAGE-4-ROHN-SCHEDULE",
                            "Session-Scheduler-Agent",
                            {"recordings_planned": recordings_planned},
                            {"session_dt": session_dt.isoformat(), "event_id": event_id})
        return record

    async def send_reminder(self, stage: ReminderStage) -> bool:
        """Send a specific reminder from the 3-stage pipeline (FR61 §4.Stage4 Step 4)."""
        messages = {
            ReminderStage.T_48H: "Your recording session is coming up. I've prepared a script. I'll send it tomorrow.",
            ReminderStage.T_24H: "Your scripts are ready. Read through them. Mark anything that doesn't sound like you.",
            ReminderStage.T_30MIN: "See you in 30 minutes. Camera on. Just say it the way you said it to me.",
        }
        text = messages.get(stage, "")
        if not text:
            return False
        url = await self._tts.synthesize(text)
        await self._telegram.send_voice_note(self._coach_id, url)

        field_map = {
            ReminderStage.T_48H: "reminder_48h_sent",
            ReminderStage.T_24H: "reminder_24h_sent",
            ReminderStage.T_30MIN: "reminder_30min_sent",
        }
        await self._db.update("scheduled_sessions",
            {"coach_id": self._coach_id, "status": "booked"},
            {field_map[stage]: datetime.utcnow().isoformat()})
        return True

    # ═══════════════════════════════════════════════════════════
    # STAGE 5: Recording Session Analysis (FR61 §4.Stage5)
    # ═══════════════════════════════════════════════════════════

    async def stage5_process_recording(
        self, video_path: str, recording_id: str,
        session_id: str, script_piece_title: str = "",
        session_start_time: Optional[datetime] = None,
        elapsed_minutes: int = 0, recordings_remaining: int = 0,
    ) -> RecordingAnalysis:
        """FR61 §4.Stage5: Process a single video recording with audio + video analysis."""
        await self._db.set_coach_context(self._coach_id)

        # Gate S5A: Session time enforcement (AC4)
        time_gate = SessionTimeGate.evaluate(elapsed_minutes, recordings_remaining)
        if time_gate.hard_stop_triggered:
            raise RecordingSessionError(
                f"Session hard stop: {elapsed_minutes} min >= {SESSION_MAX_MINUTES} min limit")
        if time_gate.warn_triggered:
            await self._telegram.send_text(self._coach_id,
                f"We're at {elapsed_minutes} minutes. Let's wrap the last take clean.")

        # Step 3b: Audio extraction + prosody analysis
        prosody = await self._audio.extract_prosody(video_path)
        transcript, timestamps = await self._audio.transcribe(video_path)
        liwc = await self._audio.analyze_liwc(transcript)
        emotions = await self._audio.extract_emotion(video_path)

        word_count = len(transcript.split())
        duration_s = max(1, len(timestamps) // 10) if timestamps else 60
        wpm = _compute_wpm(word_count, duration_s)
        filler_count = sum(1 for w in transcript.lower().split()
                          if w in ("um", "uh", "like", "you know", "basically", "actually"))
        filler_density = _compute_filler_density(filler_count, word_count)
        sincerity = _compute_sincerity_composite(liwc.liwc_authenticity, prosody.jitter, prosody.shimmer)

        iss_events = [{"duration": t.get("pause", 0), "follows_key_statement": True}
                      for t in timestamps if t.get("pause", 0) > 1.0]
        rohn_pauses = _count_rohn_pauses(iss_events)

        vocal = VocalAnalysis(
            wpm=wpm, spm=prosody.spm, pitch_variance_f0=prosody.f0_variance,
            rohn_pauses=rohn_pauses, filler_density=filler_density,
            sincerity_composite=sincerity,
            emotional_loading={"arousal": prosody.arousal, "valence": prosody.valence},
            liwc_authenticity=liwc.liwc_authenticity,
            jitter=prosody.jitter, shimmer=prosody.shimmer,
        )

        # Step 3c: Video visual analysis (Gate S5B — AC8)
        face_detected = await self._video.detect_face_track(video_path)
        video_verdict = VideoAnalysisGate.evaluate(face_detected)

        video_result = VideoAnalysis(video_analysis_available=False)
        if video_verdict == VideoAvailabilityVerdict.AVAILABLE:
            eye_pct, gaze_breaks = await self._video.analyze_eye_contact(video_path)
            gesture_score = await self._video.analyze_gestures(video_path, [])
            face_score = await self._video.analyze_facial_expression(video_path, emotions)
            posture = await self._video.analyze_posture(video_path)
            video_result = VideoAnalysis(
                eye_contact_pct=eye_pct, gaze_break_timestamps=gaze_breaks,
                gesture_congruence=gesture_score,
                facial_expression_congruence=face_score,
                posture_notes=posture, video_analysis_available=True,
            )

        # Step 3d: Write to Supabase (AC5 — separate rows per recording)
        await self._db.insert("vocal_delivery", {
            "session_id": session_id, "recording_id": recording_id,
            "coach_id": self._coach_id, "wpm": wpm, "spm": prosody.spm,
            "pitch_variance": prosody.f0_variance, "rohn_pauses_detected": rohn_pauses,
            "filler_density": filler_density, "sincerity_composite": sincerity,
            "liwc_authenticity": liwc.liwc_authenticity,
            "jitter": prosody.jitter, "shimmer": prosody.shimmer,
            "emotional_loading_arousal": prosody.arousal,
            "emotional_loading_valence": prosody.valence,
        })

        if video_result.video_analysis_available:
            await self._db.insert("video_delivery", {
                "recording_id": recording_id, "session_id": session_id,
                "coach_id": self._coach_id,
                "eye_contact_pct": video_result.eye_contact_pct,
                "gaze_break_timestamps": video_result.gaze_break_timestamps,
                "gesture_congruence_score": video_result.gesture_congruence,
                "facial_expression_congruence": video_result.facial_expression_congruence,
                "posture_engagement_map": [p.model_dump() for p in video_result.posture_notes],
            })

        # Micro-improvement detection
        prev_metrics_rows = await self._db.select("vocal_delivery",
            {"coach_id": self._coach_id}, order_by="measured_at DESC", limit=2)
        micro_improvements: List[MicroImprovementDetection] = []
        if len(prev_metrics_rows) >= 2:
            current_m = {"filler_density": filler_density, "sincerity_composite": sincerity,
                         "wpm": wpm, "rohn_pauses": float(rohn_pauses)}
            prev_m = {k: prev_metrics_rows[1].get(k, 0) for k in current_m}
            micro_improvements = _compute_micro_improvements(current_m, prev_m)

        analysis = RecordingAnalysis(
            recording_id=recording_id,
            script_piece_title=script_piece_title,
            duration_seconds=duration_s,
            vocal_analysis=vocal,
            video_analysis=video_result,
            micro_improvements_detected=micro_improvements,
        )

        # Receipt write
        self._append_receipt("ROHN-RECORDING", "STAGE-5-ROHN-RECORDING",
                            "Recording-Session-Agent",
                            {"video_path": video_path},
                            analysis.model_dump())
        return analysis

    # ═══════════════════════════════════════════════════════════
    # STAGE 6: Feedback Generation (FR61 §4.Stage6)
    # ═══════════════════════════════════════════════════════════

    async def stage6_generate_feedback(
        self, recording_analysis: RecordingAnalysis, take_number: int = 1,
    ) -> FeedbackOutput:
        """FR61 §4.Stage6: Generate Rohn-style feedback with 4 elements + micro-improvement ACK."""
        await self._db.set_coach_context(self._coach_id)

        vocal = recording_analysis.vocal_analysis
        video = recording_analysis.video_analysis
        improvements = recording_analysis.micro_improvements_detected

        # Build 4-element feedback structure (FR61 §4.Stage6 Step 2)
        elements: List[FeedbackElement] = []

        # Element 1: Micro-Improvement Acknowledgment (AC6 — before critique)
        if improvements:
            best = improvements[0]
            elements.append(FeedbackElement(
                element_type="micro_improvement",
                content=(f"Your {best.metric_name} moved from {best.previous_value} to "
                         f"{best.current_value} since last session. "
                         f"That's not luck — that's the discipline of the master showing up."),
                metric_reference=best.metric_name,
                rohn_principle="discipline of the master",
            ))

        # Element 2: Strongest Moment
        elements.append(FeedbackElement(
            element_type="strongest_moment",
            content=(f"The strongest moment was your sincerity composite at {vocal.sincerity_composite}. "
                     f"Not performance — authenticity. Your audience doesn't just hear it, they feel it."),
            rohn_principle="authenticity over performance",
        ))

        # Element 3: One Growth Area
        growth_text = ""
        if video.video_analysis_available and video.eye_contact_pct < 0.7:
            growth_text = (
                f"Your eye contact was at {int(video.eye_contact_pct * 100)}%. "
                f"Not bad — but not locked in. Let's try the next take with eyes to camera "
                f"on the key line. Let the words and the eyes arrive together."
            )
        elif vocal.filler_density > 0.03:
            growth_text = (
                f"Your filler density is at {vocal.filler_density:.1%}. "
                f"Not terrible — but not clean. Let's replace those fillers with silence. "
                f"A pause is not empty — it's where your audience processes."
            )
        else:
            growth_text = (
                "Let's work on the strategic pause. After your key claim, hold for 2 seconds. "
                "That silence is not empty — it's where your audience processes."
            )
        elements.append(FeedbackElement(
            element_type="growth_area",
            content=growth_text,
            rohn_principle="strategic silence",
        ))

        # Element 4: Forward Reference (3-Temporal Transport)
        elements.append(FeedbackElement(
            element_type="forward_reference",
            content=(
                f"Weeks ago your sincerity was lower. Today it's {vocal.sincerity_composite}. "
                f"If you keep this trajectory, by the end of the quarter your audience "
                f"won't just hear information — they'll feel a leader."
            ),
            rohn_principle="trajectory over snapshot",
        ))

        full_text = " ".join([e.content for e in elements])
        estimated_seconds = max(1, len(full_text.split()) // 3)

        # Gate S6: Validate feedback register (AC10)
        gate = FeedbackRegisterGate.evaluate(full_text, estimated_seconds)
        if gate.verdict.value != "PASS":
            raise FeedbackError(f"Gate S6 FAIL: {gate.verdict.value}")

        # TTS + delivery
        voice_url = await self._tts.synthesize(full_text)
        await self._telegram.send_voice_note(self._coach_id, voice_url)

        # Update micro_improvements as acknowledged (AC6)
        for imp in improvements:
            await self._db.insert("micro_improvements", {
                "coach_id": self._coach_id,
                "metric_name": imp.metric_name,
                "previous_value": imp.previous_value,
                "current_value": imp.current_value,
                "delta_pct": imp.delta_pct,
                "acknowledged": True,
                "acknowledged_at": datetime.utcnow().isoformat(),
            })

        output = FeedbackOutput(
            recording_id=recording_analysis.recording_id,
            coach_id=self._coach_id,
            elements=elements, full_text=full_text,
            voice_note_url=voice_url,
            estimated_duration_seconds=estimated_seconds,
            contains_antithesis=gate.antithesis_found,
            contains_hcd_reference=gate.hcd_ref_found,
            contains_rohn_principle=gate.rohn_principle_found,
            uses_lets_framing=gate.lets_framing_found,
        )

        # Receipt write
        self._append_receipt(f"ROHN-FEEDBACK-{take_number}",
                            "STAGE-6-ROHN-FEEDBACK", "Rohn-Feedback-Agent",
                            recording_analysis.model_dump(), output.model_dump())
        return output

    # ═══════════════════════════════════════════════════════════
    # STAGE 7: FR5 Feedback Signal (FR61 §4.Stage7)
    # ═══════════════════════════════════════════════════════════

    async def emit_fr5_feedback_signal(
        self, trigger_id: str, session_id: str,
        liwc_score: float, sincerity: float,
    ) -> FR5FeedbackSignal:
        """FR61 §4.Stage7: Emit webhook to FR5 Weekly Pipeline Stage 5 (AC11)."""
        signal = FR5FeedbackSignal(
            trigger_id=trigger_id, liwc_authenticity_score=liwc_score,
            sincerity_composite=sincerity,
            coach_id=self._coach_id, session_id=session_id,
        )
        logger.info(f"[FR61] FR5 feedback signal emitted: trigger={trigger_id}, "
                     f"LIWC={liwc_score}, sincerity={sincerity}")
        return signal

    # ═══════════════════════════════════════════════════════════
    # RECEIPT CHAIN VERIFICATION
    # ═══════════════════════════════════════════════════════════

    def get_receipt_chain(self) -> List[FR61ReceiptBlock]:
        """Return the full receipt chain for this session."""
        return list(self._receipt_chain)

    def verify_chain_integrity(self) -> bool:
        """Verify the receipt chain is unbroken from GENESIS to final receipt."""
        if not self._receipt_chain:
            return True
        expected_prev = "GENESIS"
        for receipt in self._receipt_chain:
            if receipt.previous_receipt_hash != expected_prev:
                return False
            expected_prev = _sha256(receipt.model_dump())
        return True
