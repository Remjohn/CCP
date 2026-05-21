from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from src.ccp.models.archetype_container_runtime_models import (
    ActionableRejectionPayload,
    ArchetypeChoice,
    ArchetypeContainerManifest,
    CCFRoutingRecommendation,
    CoachResponseCapturePacket,
    CoalitionInputs,
    ContainerIntensityProfile,
    RuntimeStatus,
    SentenceAuditRecord,
    SimilarityBand,
    SflBindingStatus,
    CompositionDepthClass,
    SflFunctionBinding,
    SubliminalFunctionStackPacket,
    CompositionDepthPacket,
    VariationProfileBinding,
    ArchetypeVariationDecision,
    ArchetypeSflExecutionContract,
)

ANTI_CENTROID_THRESHOLD = 0.75
ARC_COMP_MIN_SOURCES = 3

HEDGE_PHRASES = [
    "in general", "most people", "at the end of the day", "it is what it is",
    "just be yourself", "everyone knows", "common sense", "it's all about",
    "we all need to", "the key is to", "focus on authenticity", "just focus on",
    "it goes without saying", "needless to say", "obviously", "basically",
]

ABSTRACT_UNIVERSAL_PHRASES = [
    "every business should", "all coaches need", "the market needs",
    "people just want", "success comes from", "growth mindset",
    "hustle harder", "be authentic", "add value", "follow your passion",
]

NEUTRAL_FALLBACK_INTENSITY = ContainerIntensityProfile(
    narrative_arc="witness",
    intensity_level="medium",
    pacing_profile="measured",
    emotional_job="clarify",
)


# ════════════════════════════════════════════════════════════════════════
# SentenceLedgerBuilder — deterministic sentence splitting with offsets
# ════════════════════════════════════════════════════════════════════════

class SentenceLedgerBuilder:
    """Splits transcript into sentences with stable IDs and character offsets."""

    @staticmethod
    def build(transcript: str) -> list[SentenceAuditRecord]:
        if not transcript or not transcript.strip():
            return []

        sentences: list[SentenceAuditRecord] = []
        pattern = re.compile(r'(?<=[.!?])\s+')
        parts = pattern.split(transcript.strip())
        current_offset = 0

        for idx, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue
            start = transcript.find(part, current_offset)
            if start == -1:
                start = current_offset
            end = start + len(part)
            sentence_id = f"S{idx + 1}"
            sentences.append(SentenceAuditRecord(
                sentence_id=sentence_id,
                sentence_index=idx,
                text=part,
                start_offset=start,
                end_offset=end,
                similarity_score=0.0,
                similarity_band=SimilarityBand.LOW,
                collapse_reason="pending",
            ))
            current_offset = end

        return sentences


# ════════════════════════════════════════════════════════════════════════
# AntiCentroidValidator — sentence-level genericness detection
# NOT reusing semantic_affinity_guard.py (AC6)
# ════════════════════════════════════════════════════════════════════════

class AntiCentroidValidator:
    """Sentence-level anti-centroid scoring. Rejects when similarity_score >= 0.75 (terminal band).
    Uses hedge-phrase detection, abstract universal detection, and named-specificity scoring."""

    def validate(self, sentences: list[SentenceAuditRecord]) -> list[SentenceAuditRecord]:
        for sentence in sentences:
            text_lower = sentence.text.lower()
            hedge_hits: list[str] = []
            for phrase in HEDGE_PHRASES:
                if phrase in text_lower:
                    hedge_hits.append(phrase)

            abstract_hits: list[str] = []
            for phrase in ABSTRACT_UNIVERSAL_PHRASES:
                if phrase in text_lower:
                    abstract_hits.append(phrase)

            # Named specificity: proper nouns, numbers, quotes, specific references
            named_hits: list[str] = []
            cap_words = re.findall(r'\b[A-Z][a-z]{2,}\b', sentence.text)
            first_word_match = re.match(r'^\s*[A-Z][a-z]{2,}\b', sentence.text)
            is_proper_noun = False
            if first_word_match:
                if len(cap_words) > 1:
                    is_proper_noun = True
            else:
                if len(cap_words) > 0:
                    is_proper_noun = True
            if is_proper_noun:
                named_hits.append("proper_noun_detected")
            if re.search(r'\b\d+\b', sentence.text):
                named_hits.append("numeral_detected")
            if '"' in sentence.text or "'" in sentence.text:
                named_hits.append("quoted_speech_detected")

            # Score calculation
            hedge_penalty = len(hedge_hits) * 0.15
            abstract_penalty = len(abstract_hits) * 0.25
            specificity_bonus = len(named_hits) * 0.12

            raw_score = min(1.0, max(0.0, 0.3 + hedge_penalty + abstract_penalty - specificity_bonus))

            # Determine band
            if raw_score >= ANTI_CENTROID_THRESHOLD:
                band = SimilarityBand.TERMINAL
            elif raw_score >= 0.55:
                band = SimilarityBand.HIGH
            elif raw_score >= 0.35:
                band = SimilarityBand.MEDIUM
            else:
                band = SimilarityBand.LOW

            failed = band == SimilarityBand.TERMINAL

            # Collapse reason
            reasons: list[str] = []
            if hedge_hits:
                reasons.append(f"hedge phrases: {', '.join(hedge_hits)}")
            if abstract_hits:
                reasons.append(f"abstract universals: {', '.join(abstract_hits)}")
            if not named_hits and not hedge_hits and not abstract_hits:
                reasons.append("no specific evidence or contrarian edge detected")
            collapse_reason = "; ".join(reasons) if reasons else "within acceptable specificity"

            sentence.hedge_hits = hedge_hits
            sentence.named_specificity_hits = named_hits
            sentence.similarity_score = round(raw_score, 4)
            sentence.similarity_band = band
            sentence.collapse_reason = collapse_reason
            sentence.failed = failed

        return sentences


# ════════════════════════════════════════════════════════════════════════
# ArchetypeContractRegistry — typed in-code contracts
# ════════════════════════════════════════════════════════════════════════

ARCHETYPE_CONTRACTS: dict[ArchetypeChoice, dict] = {
    ArchetypeChoice.ARC_MYTH_DEBUNK: {
        "intent": "Expose a market lie and replace it with coach-owned proof order.",
        "structural_invariants": [
            "open with the named false belief",
            "state why it persists",
            "insert coach proof or anecdote",
            "replace belief with sharper frame",
        ],
        "anti_draft_profile": [
            "do not hedge both sides equally",
            "do not replace proof with abstract consensus language",
        ],
        "distillation_funnel": [
            "preserve named enemy",
            "preserve coach-owned example",
            "compress only repetition",
        ],
        "render_targets": ["short_form_video", "carousel", "telegram_voice_teaser"],
        "activation_stances": ["high_contrast", "aggressive_certainty"],
    },
    ArchetypeChoice.ARC_ACHIEVEMENT_STORY: {
        "intent": "Narrate a specific client or coach transformation as identity proof.",
        "structural_invariants": [
            "name the person or anonymized case",
            "describe the before state concretely",
            "show the turning-point intervention",
            "describe the after state with measurable change",
        ],
        "anti_draft_profile": [
            "do not generalize the outcome",
            "do not remove the before/after contrast",
        ],
        "distillation_funnel": [
            "preserve the named transformation",
            "preserve measurable outcome",
            "compress only scene-setting",
        ],
        "render_targets": ["short_form_video", "long_form_video", "carousel"],
        "activation_stances": ["authority_proof", "testimony"],
    },
    ArchetypeChoice.ARC_OBSERVATIONAL_HUMOR: {
        "intent": "Surface an absurdity in the market or audience behavior using comedic framing.",
        "structural_invariants": [
            "name the absurd behavior or belief",
            "escalate with a concrete example",
            "land the punchline that reframes",
        ],
        "anti_draft_profile": [
            "do not soften the absurdity into advice",
            "do not explain the joke",
        ],
        "distillation_funnel": [
            "preserve the specific absurdity",
            "preserve the punchline",
            "compress setup only",
        ],
        "render_targets": ["short_form_video", "telegram_voice_teaser"],
        "activation_stances": ["irreverent", "playful_contrast"],
    },
    ArchetypeChoice.ARC_WITNESS: {
        "intent": "Reflect on a personal experience or observation without prescription.",
        "structural_invariants": [
            "state the observation",
            "provide sensory or emotional detail",
            "leave the meaning open for audience interpretation",
        ],
        "anti_draft_profile": [
            "do not moralize at the end",
            "do not convert into advice",
        ],
        "distillation_funnel": [
            "preserve the specific moment",
            "preserve emotional texture",
            "compress only repetitive phrasing",
        ],
        "render_targets": ["short_form_video", "carousel", "long_form_video"],
        "activation_stances": ["reflective", "vulnerable", "measured"],
    },
    ArchetypeChoice.ARC_CONTRAST: {
        "intent": "Juxtapose two opposing positions to sharpen the coach's stance.",
        "structural_invariants": [
            "name position A explicitly",
            "name position B explicitly",
            "show why the coach rejects one",
            "land on the chosen position with evidence",
        ],
        "anti_draft_profile": [
            "do not balance both sides equally",
            "do not end ambiguously",
        ],
        "distillation_funnel": [
            "preserve both named positions",
            "preserve the coach's verdict",
            "compress only repeated arguments",
        ],
        "render_targets": ["short_form_video", "carousel"],
        "activation_stances": ["high_contrast", "decisive"],
    },
    ArchetypeChoice.ARC_COMP: {
        "intent": "Synthesize multiple source reactions into a cohesive compilation narrative.",
        "structural_invariants": [
            "minimum 3 distinct source reactions",
            "each source contributes a unique angle",
            "thread connects sources into a progression",
            "conclusion emerges from the synthesis, not repetition",
        ],
        "anti_draft_profile": [
            "do not repeat the same point from different sources",
            "do not lose source attribution",
        ],
        "distillation_funnel": [
            "preserve each source's unique contribution",
            "preserve the synthesis thread",
            "compress only redundant transitions",
        ],
        "render_targets": ["long_form_video", "carousel"],
        "activation_stances": ["compilation", "synthesis"],
        "min_sources": 3,
    },
}


# ════════════════════════════════════════════════════════════════════════
# ArchetypeSelectionMatrix — deterministic selection
# ════════════════════════════════════════════════════════════════════════

class ArchetypeSelectionMatrix:
    """Deterministic archetype selection from coalition, mood, stance, and source-count."""

    def select(self, coalition: CoalitionInputs, mood_context: dict | None = None) -> ArchetypeChoice:
        stance = coalition.stance_polarity.lower()
        source_count = coalition.source_count

        # ARC-COMP requires >= 3 sources
        if source_count >= ARC_COMP_MIN_SOURCES and stance in ("compilation", "synthesis"):
            return ArchetypeChoice.ARC_COMP

        # Stance-based selection
        if stance in ("high_contrast", "aggressive_certainty"):
            return ArchetypeChoice.ARC_MYTH_DEBUNK
        if stance in ("authority_proof", "testimony"):
            return ArchetypeChoice.ARC_ACHIEVEMENT_STORY
        if stance in ("irreverent", "playful_contrast"):
            return ArchetypeChoice.ARC_OBSERVATIONAL_HUMOR
        if stance in ("decisive",):
            return ArchetypeChoice.ARC_CONTRAST
        if stance in ("reflective", "vulnerable", "measured"):
            return ArchetypeChoice.ARC_WITNESS

        # Family-based fallback
        family_mix_lower = [f.lower() for f in coalition.family_mix]
        if "prs" in family_mix_lower or "voc" in family_mix_lower:
            return ArchetypeChoice.ARC_MYTH_DEBUNK
        if "ach" in family_mix_lower:
            return ArchetypeChoice.ARC_ACHIEVEMENT_STORY

        return ArchetypeChoice.ARC_WITNESS


# ════════════════════════════════════════════════════════════════════════
# EvidenceConflictGateBridge — wraps ResearchSynthesisProtocol
# ════════════════════════════════════════════════════════════════════════

class EvidenceConflictGateBridge:
    """Wraps ResearchSynthesisProtocol.execute() for pre-container conflict checks."""

    def __init__(self, research_synthesis: Any = None) -> None:
        self._synthesis = research_synthesis

    def check(self, evidence_bundle: dict | None = None) -> tuple[bool, str]:
        """Returns (is_clear, gate_status). is_clear=False means terminal block."""
        if evidence_bundle is None:
            return True, "skipped_absent"

        conflict_flags = evidence_bundle.get("conflict_flags", [])
        if conflict_flags:
            for flag in conflict_flags:
                if isinstance(flag, str) and "type_3" in flag.lower():
                    return False, "blocked_type3_authenticity"
            return False, "blocked_evidence_conflict"

        if self._synthesis is not None:
            try:
                from src.ccp.models.research_synthesis_models import Step35Input
                result = self._synthesis.execute(Step35Input(
                    bundle_id=evidence_bundle.get("bundle_id", ""),
                    authenticity_score=evidence_bundle.get("authenticity_score", 0.0),
                ))
                if hasattr(result, "status") and result.status == "TERMINAL_BLOCK":
                    return False, "blocked_research_synthesis"
            except Exception:
                pass

        return True, "evidence_clear"


# ════════════════════════════════════════════════════════════════════════
# TriggerGuardBridge — reroute metadata for rejection loops
# ════════════════════════════════════════════════════════════════════════

class TriggerGuardBridge:
    """Creates reroute tokens for upstream trigger-first execution guard."""

    @staticmethod
    def create_reroute_token(trigger_guard_session_id: str | None) -> str | None:
        if trigger_guard_session_id:
            return f"TG-REROUTE-{uuid4().hex[:8].upper()}"
        return None


class SflCrosswalkResolver:
    @staticmethod
    def resolve(
        archetype: ArchetypeChoice,
        sfl_registry: Any = None,
        binding_surface: str = "short_form_video"
    ) -> SubliminalFunctionStackPacket:
        stack_id = f"SFL-STK-{uuid4().hex[:8].upper()}"
        crosswalk_source_id = f"SFL-XW-AR-{uuid4().hex[:8].upper()}"
        active_functions = []

        if sfl_registry is not None:
            try:
                crosswalks = sfl_registry.get_crosswalk_bundle("archetype_to_function_profile")
                resolved_record = None
                for record in crosswalks.values():
                    for link in record.archetype_links:
                        name_norm = link.archetype_name.strip().lower().replace("_", "-")
                        arch_norm = archetype.value.strip().lower().replace("_", "-")
                        if name_norm == arch_norm or name_norm == arch_norm.replace("arc-", ""):
                            resolved_record = record
                            break
                    if resolved_record:
                        break

                if resolved_record:
                    crosswalk_source_id = resolved_record.artifact_id
                    pref_ids = resolved_record.preferred_function_ids
                    if pref_ids:
                        weight_slice = round(0.8 / len(pref_ids), 2)
                        for fn_id in pref_ids:
                            fn_def = sfl_registry.functions.get(fn_id)
                            if fn_def:
                                active_functions.append(SflFunctionBinding(
                                    function_id=fn_id,
                                    family_id=fn_def.family_id,
                                    canonical_name=fn_def.canonical_name,
                                    polarity=fn_def.polarities[0] if fn_def.polarities else "positive",
                                    weight=weight_slice,
                                    binding_rationale=f"Resolved from registry crosswalk {crosswalk_source_id} for {archetype.value}"
                                ))
            except Exception:
                pass

        if not active_functions:
            if archetype == ArchetypeChoice.ARC_MYTH_DEBUNK:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-001",
                        family_id="SFL-FAM-001",
                        canonical_name="Contrast Framing",
                        polarity="positive",
                        weight=0.45,
                        binding_rationale="High-contrast stance demands perceptual opposition framing"
                    ),
                    SflFunctionBinding(
                        function_id="SFL-FN-007",
                        family_id="SFL-FAM-003",
                        canonical_name="Symbolic Compression",
                        polarity="positive",
                        weight=0.35,
                        binding_rationale="Myth debunk requires compressed symbolic payload"
                    )
                ]
            elif archetype == ArchetypeChoice.ARC_ACHIEVEMENT_STORY:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-002",
                        family_id="SFL-FAM-002",
                        canonical_name="Identity Proof",
                        polarity="positive",
                        weight=0.8,
                        binding_rationale="Narrate client identity transformation with high trust"
                    )
                ]
            elif archetype == ArchetypeChoice.ARC_OBSERVATIONAL_HUMOR:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-003",
                        family_id="SFL-FAM-004",
                        canonical_name="Absurdity Escalation",
                        polarity="positive",
                        weight=0.7,
                        binding_rationale="Comedic escalation of market absurdities"
                    )
                ]
            elif archetype == ArchetypeChoice.ARC_WITNESS:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-004",
                        family_id="SFL-FAM-005",
                        canonical_name="Reflective Openness",
                        polarity="positive",
                        weight=0.6,
                        binding_rationale="Sensorially rich personal narrative without explicit moralizing"
                    )
                ]
            elif archetype == ArchetypeChoice.ARC_CONTRAST:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-005",
                        family_id="SFL-FAM-006",
                        canonical_name="Stance Juxtaposition",
                        polarity="positive",
                        weight=0.75,
                        binding_rationale="Juxtapose position A and B to force decisive alignment"
                    )
                ]
            else:
                active_functions = [
                    SflFunctionBinding(
                        function_id="SFL-FN-006",
                        family_id="SFL-FAM-007",
                        canonical_name="Synthesis Threading",
                        polarity="positive",
                        weight=0.9,
                        binding_rationale="Threading 3+ source views into compiled alignment"
                    )
                ]

        total_weight = round(sum(f.weight for f in active_functions), 2)
        return SubliminalFunctionStackPacket(
            stack_id=stack_id,
            archetype_choice=archetype,
            active_functions=active_functions,
            crosswalk_source_id=crosswalk_source_id,
            total_weight=total_weight,
            binding_surface=binding_surface,
            anti_bloat_check_passed=True
        )


class CompositionDepthResolver:
    @staticmethod
    def resolve(
        archetype: ArchetypeChoice,
        mood_context: dict | None = None
    ) -> CompositionDepthPacket:
        depth_id = f"CDP-{uuid4().hex[:8].upper()}"
        intensity = 0.5
        if mood_context:
            intensity = mood_context.get("intensity", 0.5)

        if intensity >= 0.7 and archetype in (ArchetypeChoice.ARC_MYTH_DEBUNK, ArchetypeChoice.ARC_CONTRAST):
            depth_class = CompositionDepthClass.RHYTHMIC_STRUCTURE
            rationale = "High-intensity myth debunk and contrast benefits from rhythmic acceleration"
        elif intensity <= 0.4 and archetype == ArchetypeChoice.ARC_WITNESS:
            depth_class = CompositionDepthClass.STRATEGIC_AMBIGUITY
            rationale = "Low-intensity reflective witness uses strategic ambiguity to invite interpretation"
        elif intensity >= 0.7:
            depth_class = CompositionDepthClass.LAYERED_INTERPRETATION
            rationale = "High-intensity structural framing calls for layered interpretation"
        elif intensity <= 0.4:
            depth_class = CompositionDepthClass.REPETITION_WITH_VARIATION
            rationale = "Low-intensity container defaults to repetition with variation"
        else:
            if archetype in (ArchetypeChoice.ARC_WITNESS, ArchetypeChoice.ARC_OBSERVATIONAL_HUMOR):
                depth_class = CompositionDepthClass.LAYERED_INTERPRETATION
                rationale = "Medium-intensity reflection uses layered delivery"
            else:
                depth_class = CompositionDepthClass.REPETITION_WITH_VARIATION
                rationale = "Medium-intensity delivery defaults to repetition with variation"

        return CompositionDepthPacket(
            depth_id=depth_id,
            depth_class=depth_class,
            intensity=intensity,
            cross_surface_applicable=True,
            governing_rationale=rationale
        )


class VariationAnchorBuilder:
    @staticmethod
    def resolve(
        archetype: ArchetypeChoice,
        sfl_stack: SubliminalFunctionStackPacket | None = None,
        composition_depth: CompositionDepthPacket | None = None
    ) -> tuple[VariationProfileBinding, ArchetypeVariationDecision]:
        variation_id = f"VAR-BIND-{uuid4().hex[:8].upper()}"
        decision_id = f"VAR-DEC-{uuid4().hex[:8].upper()}"

        depth_class_val = (
            composition_depth.depth_class
            if composition_depth
            else CompositionDepthClass.REPETITION_WITH_VARIATION
        )

        if archetype in (ArchetypeChoice.ARC_MYTH_DEBUNK, ArchetypeChoice.ARC_CONTRAST):
            binding = VariationProfileBinding(
                variation_id=variation_id,
                asymmetry_target=0.7,
                resonance_spacing=0.5,
                predictability_break_threshold=0.6,
                paradox_retention=False,
                variation_rationale="High-contrast stances require sharp asymmetry and predictable break thresholds without paradox retention."
            )
            applied_axes = ["asymmetry", "predictability_break"]
            decision_rationale = f"Determined variation profile matching {archetype.value} stance constraints."
        elif archetype == ArchetypeChoice.ARC_WITNESS:
            binding = VariationProfileBinding(
                variation_id=variation_id,
                asymmetry_target=0.4,
                resonance_spacing=0.8,
                predictability_break_threshold=0.5,
                paradox_retention=True,
                variation_rationale="Witness reflections benefit from high resonance spacing and paradox retention."
            )
            applied_axes = ["resonance", "paradox"]
            decision_rationale = f"Witness reflection requires paradox retention and deep resonance spacing."
        else:
            binding = VariationProfileBinding(
                variation_id=variation_id,
                asymmetry_target=0.5,
                resonance_spacing=0.5,
                predictability_break_threshold=0.4,
                paradox_retention=False,
                variation_rationale="Default variation parameters balancing pace and clarity."
            )
            applied_axes = ["asymmetry"]
            decision_rationale = "Balanced default variation anchors."

        decision = ArchetypeVariationDecision(
            decision_id=decision_id,
            archetype_choice=archetype,
            applied_axes=applied_axes,
            variation_binding=binding,
            depth_class_influence=depth_class_val,
            decision_rationale=decision_rationale
        )
        return binding, decision


class ExecutionContractAssembler:
    @staticmethod
    def assemble(
        manifest: ArchetypeContainerManifest,
        session_id: str
    ) -> ArchetypeSflExecutionContract | None:
        if not (manifest.sfl_function_stack and manifest.composition_depth and manifest.variation_binding):
            return None

        contract_id = f"CON-{uuid4().hex[:8].upper()}"

        dspy_signature_fields = {
            "input_transcript": "dspy.InputField",
            "structural_invariants": "dspy.InputField",
            "sfl_function_stack": "dspy.InputField",
            "composition_depth": "dspy.InputField",
            "variation_binding": "dspy.InputField",
            "output_rendered_blueprint": "dspy.OutputField"
        }

        coalition_family_mix = [manifest.coalition_inputs.intended_business_job]

        return ArchetypeSflExecutionContract(
            contract_id=contract_id,
            runtime_session_id=session_id,
            archetype_choice=manifest.selected_archetype,
            structural_invariants=manifest.structural_invariants,
            anti_draft_profile=manifest.anti_draft_profile,
            sfl_function_stack=manifest.sfl_function_stack,
            composition_depth=manifest.composition_depth,
            variation_binding=manifest.variation_binding,
            intensity_profile=manifest.intensity_profile,
            coalition_family_mix=coalition_family_mix,
            authorized_render_targets=manifest.authorized_render_targets,
            dspy_signature_fields=dspy_signature_fields,
            skill_execution_mode="typed_dspy_module"
        )


# ════════════════════════════════════════════════════════════════════════
# ArchetypeContainerRuntimeService — the main runtime
# ════════════════════════════════════════════════════════════════════════

class ArchetypeContainerRuntimeService:
    """Sits between CoachResponseCapture and CMF. Performs 6 deterministic jobs:
    1. Validate inputs
    2. Evidence conflict check
    3. Sentence-level anti-centroid validation
    4. Emit actionable rejection OR
    5. Select archetype and build container manifest
    6. Emit success-grade CCFRoutingRecommendation"""

    def __init__(self, supabase_client: Any = None, receipt_chain: Any = None, research_synthesis: Any = None, psych_routing: Any = None, sfl_registry: Any = None, sda_query: Any = None) -> None:
        self._supabase = supabase_client
        self._receipt_chain = receipt_chain
        self._evidence_gate = EvidenceConflictGateBridge(research_synthesis)
        self._psych_routing = psych_routing
        self._validator = AntiCentroidValidator()
        self._matrix = ArchetypeSelectionMatrix()
        self._sfl_registry = sfl_registry
        self._sda_query = sda_query

    async def compile(self, *, capture: CoachResponseCapturePacket, coalition: CoalitionInputs, mood_context: dict | None = None, evidence_bundle: dict | None = None, sfl_function_stack: SubliminalFunctionStackPacket | None = None, composition_depth: CompositionDepthPacket | None = None, variation_profile: VariationProfileBinding | None = None) -> CCFRoutingRecommendation:
        session_id = f"ACR-SESSION-{uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        # Receipt: compile start
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="compile-start", metadata={"session_id": session_id, "coach_id": capture.coach_id, "capture_id": capture.capture_id})

        # Step 1: Evidence conflict check
        is_clear, gate_status = self._evidence_gate.check(evidence_bundle)
        if self._receipt_chain is not None:
            self._receipt_chain.log(action="evidence-clear", metadata={"session_id": session_id, "gate_status": gate_status})

        if not is_clear:
            return self._build_blocked_recommendation(session_id, capture.coach_id, now)

        # Step 2: Sentence ledger
        sentences = SentenceLedgerBuilder.build(capture.transcript_text)
        if not sentences:
            return self._build_blocked_recommendation(session_id, capture.coach_id, now)

        # Step 3: Anti-centroid validation
        audited = self._validator.validate(sentences)
        failing = [s for s in audited if s.failed]

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="sentence-audit", metadata={"session_id": session_id, "total_sentences": len(audited), "failing_count": len(failing)})

        # Persist sentence audits
        if self._supabase is not None:
            for s in audited:
                try:
                    self._supabase.table("archetype_runtime_sentence_audits").insert({
                        "sentence_audit_id": f"{session_id}-{s.sentence_id}",
                        "runtime_session_id": session_id,
                        "sentence_id": s.sentence_id,
                        "sentence_index": s.sentence_index,
                        "sentence_text": s.text,
                        "start_offset": s.start_offset,
                        "end_offset": s.end_offset,
                        "similarity_score": s.similarity_score,
                        "similarity_band": s.similarity_band.value,
                        "collapse_reason": s.collapse_reason,
                        "failed": s.failed,
                    }).execute()
                except Exception:
                    pass

        # Step 4: Rejection if any sentence is terminal
        if failing:
            max_score = max(s.similarity_score for s in failing)
            coaching_fix = self._generate_coaching_fix(failing)
            rerecord_prompt = self._generate_rerecord_prompt(failing, audited)
            reroute_token = TriggerGuardBridge.create_reroute_token(capture.trigger_guard_session_id)

            rejection = ActionableRejectionPayload(
                runtime_session_id=session_id,
                rejection_code="ANTI_CENTROID_COLLAPSE",
                similarity_score=max_score,
                similarity_band=SimilarityBand.TERMINAL,
                failing_sentence_ids=[s.sentence_id for s in failing],
                failing_sentences=[s.text for s in failing],
                collapse_reasons=[s.collapse_reason for s in failing],
                coaching_fix=coaching_fix,
                rerecord_prompt=rerecord_prompt,
                trigger_guard_reroute_token=reroute_token,
                trigger_guard_session_id=capture.trigger_guard_session_id,
            )

            if self._receipt_chain is not None:
                self._receipt_chain.log(action="rejection", metadata={"session_id": session_id, "rejection_code": "ANTI_CENTROID_COLLAPSE", "failing_count": len(failing)})

            # Persist rejection
            if self._supabase is not None:
                try:
                    self._supabase.table("archetype_runtime_rejections").insert({
                        "rejection_id": f"{session_id}-REJ",
                        "runtime_session_id": session_id,
                        "rejection_code": "ANTI_CENTROID_COLLAPSE",
                        "similarity_score": max_score,
                        "coaching_fix": coaching_fix,
                        "rerecord_prompt": rerecord_prompt,
                        "reroute_token": reroute_token,
                    }).execute()
                except Exception:
                    pass

            downstream_targets = ["trigger_first_execution_guard"] if capture.trigger_guard_session_id else []

            recommendation = CCFRoutingRecommendation(
                runtime_session_id=session_id,
                coach_id=capture.coach_id,
                status=RuntimeStatus.REJECTED_ACTIONABLE,
                rejection_payload=rejection,
                downstream_family_targets=[],
                downstream_system_targets=downstream_targets,
                receipt_chain_hash=f"RCP-{uuid4().hex[:6].upper()}",
                generated_at=now,
            )

            self._persist_session(session_id, capture, coalition, recommendation)
            return recommendation

        # Step 5: Archetype selection
        selected = self._matrix.select(coalition, mood_context)

        # ARC-COMP guard (AC5)
        if selected == ArchetypeChoice.ARC_COMP and coalition.source_count < ARC_COMP_MIN_SOURCES:
            selected = ArchetypeChoice.ARC_WITNESS

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="container-select", metadata={"session_id": session_id, "selected_archetype": selected.value})

        # Step 6: Build manifest
        contract = ARCHETYPE_CONTRACTS[selected]
        intensity = self._resolve_intensity(mood_context, selected)
        accepted_ids = [s.sentence_id for s in audited if not s.failed]

        # SFL binding validation & resolution
        if composition_depth is not None:
            if not isinstance(composition_depth.depth_class, CompositionDepthClass):
                try:
                    CompositionDepthClass(composition_depth.depth_class)
                except ValueError:
                    raise ValueError(f"Invalid depth_class: {composition_depth.depth_class}")

        sfl_registry_available = self._sfl_registry is not None
        sfl_registry_ready = False
        if sfl_registry_available:
            try:
                if hasattr(self._sfl_registry, "health"):
                    health = self._sfl_registry.health()
                    if hasattr(health, "ready"):
                        sfl_registry_ready = health.ready
                    else:
                        sfl_registry_ready = True
                else:
                    sfl_registry_ready = True
            except Exception:
                pass

        bound_sfl_stack = sfl_function_stack
        bound_depth = composition_depth
        bound_variation = variation_profile
        bound_decision = None

        if sfl_registry_available and sfl_registry_ready:
            if bound_sfl_stack is None:
                bound_sfl_stack = SflCrosswalkResolver.resolve(selected, self._sfl_registry, binding_surface=coalition.intended_business_job)
            if bound_depth is None:
                bound_depth = CompositionDepthResolver.resolve(selected, mood_context)
            if bound_variation is None:
                bound_variation, bound_decision = VariationAnchorBuilder.resolve(selected, bound_sfl_stack, bound_depth)

            if self._receipt_chain is not None:
                self._receipt_chain.log(action="sfl_bind", metadata={"stack_id": bound_sfl_stack.stack_id, "active_functions": [f.function_id for f in bound_sfl_stack.active_functions]})
                self._receipt_chain.log(action="composition_bind", metadata={"depth_id": bound_depth.depth_id, "depth_class": bound_depth.depth_class.value})
                self._receipt_chain.log(action="variation_bind", metadata={"variation_id": bound_variation.variation_id, "asymmetry_target": bound_variation.asymmetry_target})

            sfl_binding_status = SflBindingStatus.SFL_BOUND
        else:
            passed_count = sum(1 for x in (sfl_function_stack, composition_depth, variation_profile) if x is not None)
            if passed_count == 3:
                sfl_binding_status = SflBindingStatus.SFL_BOUND
            elif passed_count > 0:
                sfl_binding_status = SflBindingStatus.SFL_PARTIAL
            else:
                if self._sfl_registry is not None:
                    sfl_binding_status = SflBindingStatus.SFL_UNAVAILABLE
                    if self._receipt_chain is not None:
                        self._receipt_chain.log(action="sfl_bind_skipped", metadata={"reason": "registry_unavailable"})
                else:
                    sfl_binding_status = SflBindingStatus.SFL_NOT_BOUND
                    if self._receipt_chain is not None:
                        self._receipt_chain.log(action="sfl_bind_skipped", metadata={"reason": "no_sfl_inputs"})

            if bound_sfl_stack and self._receipt_chain:
                self._receipt_chain.log(action="sfl_bind", metadata={"stack_id": bound_sfl_stack.stack_id})
            if bound_depth and self._receipt_chain:
                self._receipt_chain.log(action="composition_bind", metadata={"depth_id": bound_depth.depth_id})
            if bound_variation and self._receipt_chain:
                self._receipt_chain.log(action="variation_bind", metadata={"variation_id": bound_variation.variation_id})

        if bound_variation is not None and bound_decision is None:
            _, bound_decision = VariationAnchorBuilder.resolve(selected, bound_sfl_stack, bound_depth)

        container_id = f"ACR-CONTAINER-{uuid4().hex[:8].upper()}"
        manifest = ArchetypeContainerManifest(
            runtime_session_id=session_id,
            container_id=container_id,
            selected_archetype=selected,
            archetype_intent=contract["intent"],
            activation_condition_summary=f"{coalition.stance_polarity} stance + {coalition.source_count} source(s) + {coalition.evidence_strength:.2f} evidence strength.",
            structural_invariants=contract["structural_invariants"],
            anti_draft_profile=contract["anti_draft_profile"],
            distillation_funnel=contract["distillation_funnel"],
            accepted_sentence_ids=accepted_ids,
            coalition_inputs=coalition,
            intensity_profile=intensity,
            cmf_render_hints=self._generate_render_hints(selected, intensity),
            authorized_render_targets=contract["render_targets"],
            created_at=now,
            sfl_function_stack=bound_sfl_stack,
            composition_depth=bound_depth,
            variation_binding=bound_variation,
            variation_decision=bound_decision,
            sfl_binding_status=sfl_binding_status
        )

        if sfl_binding_status == SflBindingStatus.SFL_BOUND:
            exec_contract = ExecutionContractAssembler.assemble(manifest, session_id)
            manifest.execution_contract = exec_contract
            if exec_contract and self._receipt_chain is not None:
                self._receipt_chain.log(action="execution_contract_assembled", metadata={"contract_id": exec_contract.contract_id})

        # Persist manifest
        if self._supabase is not None:
            try:
                manifest_data = {
                    "container_id": container_id,
                    "runtime_session_id": session_id,
                    "coach_id": capture.coach_id,
                    "selected_archetype": selected.value,
                    "manifest_json": manifest.model_dump(mode="json"),
                    "sfl_binding_status": manifest.sfl_binding_status.value,
                }
                if manifest.sfl_function_stack:
                    manifest_data["sfl_function_stack_json"] = manifest.sfl_function_stack.model_dump(mode="json")
                if manifest.composition_depth:
                    manifest_data["composition_depth_json"] = manifest.composition_depth.model_dump(mode="json")
                if manifest.variation_binding:
                    manifest_data["variation_binding_json"] = manifest.variation_binding.model_dump(mode="json")
                self._supabase.table("archetype_container_manifests").insert(manifest_data).execute()

                if manifest.execution_contract is not None:
                    self._supabase.table("archetype_sfl_execution_contracts").insert({
                        "contract_id": manifest.execution_contract.contract_id,
                        "runtime_session_id": session_id,
                        "archetype_choice": selected.value,
                        "contract_json": manifest.execution_contract.model_dump(mode="json"),
                        "sfl_binding_status": manifest.sfl_binding_status.value,
                    }).execute()
            except Exception:
                pass

        if self._receipt_chain is not None:
            self._receipt_chain.log(action="cmf-hand-off", metadata={"session_id": session_id, "container_id": container_id, "selected_archetype": selected.value})

        recommendation = CCFRoutingRecommendation(
            runtime_session_id=session_id,
            coach_id=capture.coach_id,
            status=RuntimeStatus.COMPILED,
            selected_archetype=selected,
            container_manifest=manifest,
            downstream_family_targets=[coalition.intended_business_job],
            downstream_system_targets=["cmf_arc_governed_rendering"],
            receipt_chain_hash=f"RCP-{uuid4().hex[:6].upper()}",
            generated_at=now,
            sfl_binding_status=sfl_binding_status,
        )

        self._persist_session(session_id, capture, coalition, recommendation)
        return recommendation

    def _build_blocked_recommendation(self, session_id: str, coach_id: str, now: datetime) -> CCFRoutingRecommendation:
        return CCFRoutingRecommendation(
            runtime_session_id=session_id,
            coach_id=coach_id,
            status=RuntimeStatus.BLOCKED_EVIDENCE_CONFLICT,
            downstream_family_targets=[],
            downstream_system_targets=[],
            receipt_chain_hash=f"RCP-{uuid4().hex[:6].upper()}",
            generated_at=now,
        )

    def _resolve_intensity(self, mood_context: dict | None, archetype: ArchetypeChoice) -> ContainerIntensityProfile:
        if mood_context is None:
            return NEUTRAL_FALLBACK_INTENSITY

        intensity_val = mood_context.get("intensity", 0.5)
        primary_vector = mood_context.get("primary_vector", "neutral")

        if intensity_val >= 0.7:
            return ContainerIntensityProfile(
                narrative_arc="confrontation" if archetype in (ArchetypeChoice.ARC_MYTH_DEBUNK, ArchetypeChoice.ARC_CONTRAST) else "escalation",
                intensity_level="high",
                pacing_profile="tight_accelerating",
                emotional_job=f"amplify_{primary_vector}",
            )
        elif intensity_val >= 0.4:
            return ContainerIntensityProfile(
                narrative_arc="build",
                intensity_level="medium",
                pacing_profile="measured",
                emotional_job=f"sustain_{primary_vector}",
            )
        else:
            return ContainerIntensityProfile(
                narrative_arc="witness",
                intensity_level="low",
                pacing_profile="slow_reflective",
                emotional_job="clarify",
            )

    def _generate_coaching_fix(self, failing: list[SentenceAuditRecord]) -> str:
        hedge_total = sum(len(s.hedge_hits) for s in failing)
        named_total = sum(len(s.named_specificity_hits) for s in failing)
        if hedge_total > 0 and named_total == 0:
            return "Replace the generic advice with one named client moment or one explicit claim you believe the market gets wrong."
        elif hedge_total > 0:
            return "Remove the hedging language and commit to the specific claim you are making."
        else:
            return "Add a concrete example, a named case, or a specific number that grounds your point beyond abstract advice."

    def _generate_rerecord_prompt(self, failing: list[SentenceAuditRecord], all_sentences: list[SentenceAuditRecord]) -> str:
        if not failing:
            return "Re-record with more specificity."
        last_good_idx = 0
        for s in all_sentences:
            if s.sentence_id == failing[0].sentence_id:
                break
            last_good_idx = s.sentence_index
        last_good_id = f"S{last_good_idx + 1}" if last_good_idx > 0 else "the beginning"
        return f"Re-record the section after sentence {last_good_id}. Name the exact belief you reject and the client moment that made you reject it."

    def _generate_render_hints(self, archetype: ArchetypeChoice, intensity: ContainerIntensityProfile) -> list[str]:
        hints = []
        if intensity.intensity_level == "high":
            hints.append("high-contrast close-up start")
            hints.append("fast proof turn after accusation")
        elif intensity.intensity_level == "medium":
            hints.append("medium-distance framing")
            hints.append("steady pacing through build")
        else:
            hints.append("soft opening with ambient texture")
            hints.append("allow pauses for reflection")

        if archetype == ArchetypeChoice.ARC_MYTH_DEBUNK:
            hints.append("bold text overlay on named false belief")
        elif archetype == ArchetypeChoice.ARC_ACHIEVEMENT_STORY:
            hints.append("before/after visual split if available")

        return hints

    def _persist_session(self, session_id: str, capture: CoachResponseCapturePacket, coalition: CoalitionInputs, recommendation: CCFRoutingRecommendation) -> None:
        if self._supabase is not None:
            try:
                self._supabase.table("archetype_runtime_sessions").insert({
                    "runtime_session_id": session_id,
                    "coach_id": capture.coach_id,
                    "capture_id": capture.capture_id,
                    "coalition_id": coalition.coalition_id,
                    "runtime_status": recommendation.status.value,
                    "selected_archetype": recommendation.selected_archetype.value if recommendation.selected_archetype else None,
                    "trigger_guard_session_id": capture.trigger_guard_session_id,
                    "receipt_chain_hash": recommendation.receipt_chain_hash,
                }).execute()
            except Exception:
                pass
