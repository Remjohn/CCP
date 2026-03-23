"""
FR-VIS-01 — Visual Composition Brief Generation
=================================================
Abel's 9-step sequential decision process for producing a complete VCB
that deterministically maps script psychological intent to per-slide
visual parameters.

Pipeline stages:
  Stage 1 — Format Determination & Recipe Selection (Steps 1-2)
  Stage 2 — PSSL Parameter Assignment (Step 3)
  Stage 3 — TIAR Query & Tribal Noun Pairing (Step 4)
  Stage 4 — Handle Bar, Semantic Conflict, Accumulation, Semiotic (Steps 5-8)
  Stage 5 — Gate C-09 Validation (Step 9)
"""

from __future__ import annotations

import math
import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.visual_engine_models import (
    AccumulationAudit,
    AccumulationAuditStatus,
    COMPLETION_IMAGERY_KEYWORDS,
    GAZE_CBCS_COLD_THRESHOLD,
    GAZE_CBCS_WARM_THRESHOLD,
    GAZE_ZONE_RANGES,
    GateC09CheckResult,
    GateC09Result,
    GateC09Rule,
    GateC09Verdict,
    GazeTargetZone,
    HandleBarConfig,
    MAX_INTERNAL_REVISIONS,
    MIN_TIAR_NOUNS_PER_TEXT_SLIDE,
    MOOD_COLOR_TEMPERATURE,
    MOOD_SATURATION_ANCHORS,
    MoodState,
    PADVector,
    PerSlideAssignment,
    PSSLBlock,
    SEMIOTIC_INJECTION_EARLIEST_RATIO,
    SEMIOTIC_INJECTION_MIN_SLIDES,
    SemanticConflict,
    SemanticConflictType,
    SemioticInjection,
    SomaticArcType,
    TribalNounAssignment,
    VCBError,
    VCBGenerationInput,
    VisualCompositionBrief,
)

# ────────────────────────────────────────────────────────────────────────
# Agent name constant — C-11 persona masking: the agent label is used
# only internally for receipt writes, NEVER in any API payload.
# ────────────────────────────────────────────────────────────────────────
_AGENT_ID = "abel_vcb_generator"


class AbelVCBGenerator:
    """
    Abel (Visual Composition Planner) — complete 9-step VCB generator.

    Parameters
    ----------
    coach_acronym : str
        2-4 character coach identifier (ADR-01).
    receipt_chain : ReceiptChain
        Shared receipt chain for audit logging.
    """

    # ------------------------------------------------------------------ #
    # Construction
    # ------------------------------------------------------------------ #

    def __init__(
        self,
        coach_acronym: str,
        receipt_chain: ReceiptChain,
    ) -> None:
        if not (2 <= len(coach_acronym) <= 4):
            raise ValueError(
                f"coach_acronym must be 2-4 characters, got '{coach_acronym}'"
            )
        self._coach = coach_acronym
        self._rc = receipt_chain

    # ================================================================== #
    # PUBLIC API
    # ================================================================== #

    def generate(self, inp: VCBGenerationInput) -> VisualCompositionBrief:
        """
        Execute the full 9-step VCB generation process.

        Returns a complete ``VisualCompositionBrief`` that has passed
        Gate C-09 validation.
        """
        warnings: list[str] = []

        # Legacy fallback (§6)
        if not inp.has_psychological_routing_brief:
            inp = inp.model_copy(
                update={
                    "mood_state": MoodState.PROCESSING,
                    "cbcs_score": 4,
                    "has_psychological_routing_brief": False,
                },
            )
            warnings.append(VCBError.LEGACY_ROUTING_DEFAULT)

        # -- Stage 1: Format & Recipe --------------------------------- #
        recipe_id = inp.recipe_id or self._select_recipe(inp)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="stage_1_format_recipe",
            asset_id=inp.content_output_id,
            output_summary=f"recipe={recipe_id}, format={inp.content_format}",
        )

        # -- Stage 2: PSSL assignment --------------------------------- #
        pssl_blocks = self._assign_pssl(inp)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="stage_2_pssl_assignment",
            asset_id=inp.content_output_id,
            output_summary=f"slides={len(pssl_blocks)}",
        )

        # -- Stage 3: TIAR noun pairing ------------------------------- #
        noun_assignments = self._assign_tribal_nouns(inp)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="stage_3_tiar_pairing",
            asset_id=inp.content_output_id,
            output_summary=f"noun_sets={len(noun_assignments)}",
        )

        # -- Stage 4 steps -------------------------------------------- #
        handle_bars = self._assign_handle_bars(inp)
        semantic_conflicts = self._build_semantic_conflicts(inp)
        accumulation_audit = self._run_accumulation_audit(inp, pssl_blocks)
        semiotic = self._place_semiotic_injection(inp)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="stage_4_composition",
            asset_id=inp.content_output_id,
            output_summary=(
                f"handle_bars={len(handle_bars)}, "
                f"acc_status={accumulation_audit.audit_status}"
            ),
        )

        # -- Assemble per-slide assignments ---------------------------- #
        slides: list[PerSlideAssignment] = []
        for i in range(inp.slide_count):
            slide_type = self._classify_slide(i, inp)
            slides.append(
                PerSlideAssignment(
                    slide_index=i,
                    slide_type=slide_type,
                    image_type=self._default_image_type(i, inp),
                    pssl=pssl_blocks[i],
                    tribal_noun_assignments=(
                        noun_assignments[i] if i < len(noun_assignments) else []
                    ),
                    handle_bar=handle_bars[i] if i < len(handle_bars) else HandleBarConfig(visible=False, position=None),
                    semantic_conflicts=(
                        semantic_conflicts.get(i, [])
                    ),
                    named_person_reference=None,
                )
            )

        # -- Stage 5: Gate C-09 with internal revision loop ------------ #
        vcb_id = f"VCB-{self._coach}-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        ts = datetime.now(timezone.utc).isoformat()

        gate_result: GateC09Result | None = None
        for revision in range(MAX_INTERNAL_REVISIONS + 1):
            gate_result = self._run_gate_c09(slides, inp, semiotic)
            if gate_result.verdict == GateC09Verdict.PASS:
                break
            # Auto-revise
            slides = self._auto_revise(slides, gate_result, inp)
            gate_result = gate_result.model_copy(
                update={"revision_count": revision + 1},
            )

        if gate_result is None:
            gate_result = GateC09Result(verdict=GateC09Verdict.ESCALATED, escalated=True)

        if gate_result.verdict != GateC09Verdict.PASS:
            gate_result = gate_result.model_copy(
                update={
                    "verdict": GateC09Verdict.ESCALATED,
                    "escalated": True,
                },
            )
            warnings.append(VCBError.GATE_C09_EXCEEDED_REVISIONS)

        self._rc.log(
            agent_id=_AGENT_ID,
            action="stage_5_gate_c09",
            asset_id=inp.content_output_id,
            output_summary=f"verdict={gate_result.verdict}, revisions={gate_result.revision_count}",
        )

        vcb = VisualCompositionBrief(
            vcb_id=vcb_id,
            content_output_id=inp.content_output_id,
            coach_acronym=inp.coach_acronym,
            content_format=inp.content_format,
            selected_recipe_id=recipe_id,
            somatic_arc_type=inp.somatic_arc_type,
            slide_count=inp.slide_count,
            format_envelope_id=inp.format_envelope_id,
            style_directive_id=inp.style_directive_id,
            visual_style=inp.visual_style,
            mood_state=inp.mood_state,
            cbcs_score=inp.cbcs_score,
            per_slide_assignments=slides,
            accumulation_audit=accumulation_audit,
            semiotic_injection=semiotic,
            gate_c09_result=gate_result,
            timestamp_utc=ts,
            warnings=warnings,
        )

        return vcb

    # ================================================================== #
    # STAGE 1 — FORMAT DETERMINATION & RECIPE SELECTION
    # ================================================================== #

    @staticmethod
    def _select_recipe(inp: VCBGenerationInput) -> str:
        """
        Select the best recipe for the given format / style / mood.
        In a full implementation this queries DEP-VIS-002.
        Here we deterministically construct the recipe ID.
        """
        fmt = inp.content_format.upper().replace(" ", "_")
        style = inp.visual_style.upper().replace(" ", "_")
        return f"RCP-{fmt}-{style}-001"

    # ================================================================== #
    # STAGE 2 — PSSL PARAMETER ASSIGNMENT
    # ================================================================== #

    def _assign_pssl(self, inp: VCBGenerationInput) -> list[PSSLBlock]:
        """Produce a PSSLBlock for every slide."""
        blocks: list[PSSLBlock] = []
        anchors = MOOD_SATURATION_ANCHORS.get(inp.mood_state, (50, 65, 45))
        temp_range = MOOD_COLOR_TEMPERATURE.get(inp.mood_state, (5000, 5500))
        gaze_zone = self._resolve_gaze_zone(inp.cbcs_score)
        pupil = self._pupil_for_zone(gaze_zone)
        head_rot = self._head_rotation_for_zone(gaze_zone)

        for i in range(inp.slide_count):
            sat = self._saturation_for_slide(i, inp.slide_count, inp.somatic_arc_type, anchors)
            blocks.append(
                PSSLBlock(
                    lighting_grammar=self._lighting_grammar(i, temp_range, sat),
                    saturation_pct=sat,
                    head_rotation_degrees=head_rot,
                    pupil_position_ratio_pct=pupil,
                    pad_environmental_grammar=self._pad_for_mood(inp.mood_state, i, inp.slide_count),
                    chromatic_bloom_sequence=[self._bloom_entry(i, temp_range)],
                    incomplete_tribal_artifact=self._incomplete_artifact(
                        i, inp.slide_count, inp.somatic_arc_type,
                    ),
                )
            )
        return blocks

    # ---- PSSL helpers ------------------------------------------------ #

    @staticmethod
    def _saturation_for_slide(
        index: int,
        total: int,
        arc: str,
        anchors: tuple[int, int, int],
    ) -> int:
        """
        Compute per-slide saturation along the somatic arc curve.
        Tension arcs: rise to peak then drop.
        Discovery: steady rise.
        Contrast: oscillate.
        Accumulation: rise steeply then cliff.
        """
        low, peak, release = anchors
        if total <= 1:
            return peak

        progress = index / (total - 1)  # 0.0 → 1.0

        if arc in (SomaticArcType.TENSION_RELEASE, SomaticArcType.TENSION_RELEASE.value):
            # Peak around 60 % of the way through
            peak_point = 0.6
            if progress <= peak_point:
                t = progress / peak_point
                return round(low + (peak - low) * t)
            else:
                t = (progress - peak_point) / (1.0 - peak_point)
                return round(peak - (peak - release) * t)

        if arc in (SomaticArcType.DISCOVERY_REVELATION, SomaticArcType.DISCOVERY_REVELATION.value):
            return round(low + (peak - low) * progress)

        if arc in (SomaticArcType.CONTRAST_RESOLUTION, SomaticArcType.CONTRAST_RESOLUTION.value):
            # Alternate high/low
            if index % 2 == 0:
                return peak
            return low

        if arc in (SomaticArcType.ACCUMULATION_CLIFF, SomaticArcType.ACCUMULATION_CLIFF.value):
            # Build steeply, cliff on last slide
            if index == total - 1:
                return release
            t = progress / max((total - 2) / (total - 1), 0.01)
            t = min(t, 1.0)
            return round(low + (peak - low) * t)

        # Fallback
        return round(low + (peak - low) * progress)

    @staticmethod
    def _resolve_gaze_zone(cbcs: int) -> str:
        if cbcs < GAZE_CBCS_COLD_THRESHOLD:
            return GazeTargetZone.HOOK
        if cbcs >= GAZE_CBCS_WARM_THRESHOLD:
            return GazeTargetZone.ACTION
        return GazeTargetZone.HOOK  # mid-range defaults to Hook

    @staticmethod
    def _pupil_for_zone(zone: str) -> float:
        lo, hi = GAZE_ZONE_RANGES.get(zone, (35.0, 45.0))
        return round((lo + hi) / 2, 1)

    @staticmethod
    def _head_rotation_for_zone(zone: str) -> float:
        if zone == GazeTargetZone.ACTION:
            return 20.0
        if zone == GazeTargetZone.IDENTITY:
            return 0.0
        return 12.0  # Hook zone

    @staticmethod
    def _lighting_grammar(index: int, temp_range: tuple[int, int], sat: int) -> str:
        lo, hi = temp_range
        return (
            f"golden hour lateral, temporal_signal: {lo}K-{hi}K "
            f"warm transition over 3s, shadow: {max(15, 45 - index * 5)}° "
            f"key angle, fill ratio 2:1"
        )

    @staticmethod
    def _pad_for_mood(mood: str, index: int, total: int) -> PADVector:
        base: dict[str, tuple[float, float, float]] = {
            MoodState.PROCESSING: (-0.1, 0.3, 0.2),
            MoodState.ESCAPE: (0.6, 0.7, 0.1),
            MoodState.DISCOVERY: (0.4, 0.5, 0.4),
            MoodState.STATUS: (0.2, 0.4, 0.7),
        }
        p, a, d = base.get(mood, (0.0, 0.3, 0.3))
        # Slight progression along arousal
        progress = index / max(total - 1, 1)
        a_adj = min(1.0, a + 0.2 * progress)
        return PADVector(P=round(p, 2), A=round(a_adj, 2), D=round(d, 2))

    @staticmethod
    def _bloom_entry(index: int, temp_range: tuple[int, int]) -> str:
        lo, hi = temp_range
        return f"#{lo:04X}→#{hi:04X} ease {max(1, 3 - index * 0.3):.1f}s"

    @staticmethod
    def _incomplete_artifact(index: int, total: int, arc: str) -> str | None:
        """Non-null for tension/accumulation slides (not the final release)."""
        is_tension = arc in (
            SomaticArcType.TENSION_RELEASE,
            SomaticArcType.TENSION_RELEASE.value,
            SomaticArcType.ACCUMULATION_CLIFF,
            SomaticArcType.ACCUMULATION_CLIFF.value,
        )
        if not is_tension:
            return None
        # Last slide is the release / cliff — no artifact
        if index >= total - 1:
            return None
        return "half-drawn circle"

    # ================================================================== #
    # STAGE 3 — TIAR NOUN PAIRING
    # ================================================================== #

    @staticmethod
    def _assign_tribal_nouns(
        inp: VCBGenerationInput,
    ) -> list[list[TribalNounAssignment]]:
        """
        Assign ≥ MIN_TIAR_NOUNS_PER_TEXT_SLIDE active nouns per text slide.
        """
        active = [n for n in inp.active_nouns if n not in inp.blocked_nouns]
        result: list[list[TribalNounAssignment]] = []
        positions = ["hook_text", "body_text", "subtext", "overlay_text"]

        for s in range(inp.slide_count):
            if not active:
                result.append([])
                continue
            assignments: list[TribalNounAssignment] = []
            for j in range(min(len(active), max(MIN_TIAR_NOUNS_PER_TEXT_SLIDE, 3))):
                noun = active[j % len(active)]
                assignments.append(
                    TribalNounAssignment(
                        noun=noun,
                        position=positions[j % len(positions)],
                        congruent_visual_element=f"visual congruence for '{noun}'",
                    )
                )
            result.append(assignments)
        return result

    # ================================================================== #
    # STAGE 4 — HANDLE BAR / SEMANTIC CONFLICT / ACCUMULATION / SEMIOTIC
    # ================================================================== #

    @staticmethod
    def _assign_handle_bars(inp: VCBGenerationInput) -> list[HandleBarConfig]:
        """Step 5 — Coach Handle Bar Decision."""
        bars: list[HandleBarConfig] = []
        for i in range(inp.slide_count):
            if i == 0:
                # Slide 0 always has handle bar
                bars.append(HandleBarConfig(visible=True, position="top_locked"))
            elif inp.slide_count == 1:
                bars.append(HandleBarConfig(visible=True, position="top_locked"))
            else:
                bars.append(HandleBarConfig(visible=False, position=None))
        return bars

    @staticmethod
    def _build_semantic_conflicts(
        inp: VCBGenerationInput,
    ) -> dict[int, list[SemanticConflict]]:
        """Step 6 — Semantic Conflict Specification (stub for external data)."""
        return {}

    @staticmethod
    def _run_accumulation_audit(
        inp: VCBGenerationInput,
        pssl_blocks: list[PSSLBlock],
    ) -> AccumulationAudit:
        """Step 7 — Accumulation Prohibition Audit."""
        arc = inp.somatic_arc_type
        if arc not in (
            SomaticArcType.ACCUMULATION_CLIFF,
            SomaticArcType.ACCUMULATION_CLIFF.value,
        ):
            return AccumulationAudit(
                arc_type=arc,
                audit_status=AccumulationAuditStatus.NOT_APPLICABLE,
            )

        # Accumulation slides = everything except the last (cliff)
        acc_slides = list(range(inp.slide_count - 1))
        violating: list[int] = []

        for s in acc_slides:
            block = pssl_blocks[s]
            # Check incomplete_tribal_artifact description for completion imagery
            artifact = (block.incomplete_tribal_artifact or "").lower()
            for kw in COMPLETION_IMAGERY_KEYWORDS:
                if kw in artifact:
                    violating.append(s)
                    break

        status = (
            AccumulationAuditStatus.VIOLATION_DETECTED
            if violating
            else AccumulationAuditStatus.CLEAN
        )

        return AccumulationAudit(
            arc_type=arc,
            accumulation_slides=acc_slides,
            completion_imagery_detected=bool(violating),
            violating_slides=violating,
            audit_status=status,
        )

    @staticmethod
    def _place_semiotic_injection(
        inp: VCBGenerationInput,
    ) -> SemioticInjection | None:
        """Step 8 — Semiotic Injection Positioning."""
        if inp.slide_count < SEMIOTIC_INJECTION_MIN_SLIDES:
            return None

        earliest = math.ceil(inp.slide_count * SEMIOTIC_INJECTION_EARLIEST_RATIO)
        # Default: place at earliest valid position
        injection_idx = max(earliest, 2)  # never slides 0 or 1
        if injection_idx >= inp.slide_count:
            injection_idx = inp.slide_count - 1

        return SemioticInjection(
            injection_slide_index=injection_idx,
            total_slides=inp.slide_count,
            position_valid=(injection_idx >= 2),
            injection_element="crystallization moment — symbolic transformation visual",
        )

    # ================================================================== #
    # STAGE 5 — GATE C-09 VALIDATION
    # ================================================================== #

    @staticmethod
    def _run_gate_c09(
        slides: list[PerSlideAssignment],
        inp: VCBGenerationInput,
        semiotic: SemioticInjection | None,
    ) -> GateC09Result:
        """Execute all 7 Gate C-09 rules and return aggregate result."""
        checks: list[GateC09CheckResult] = []
        violations: list[str] = []

        # C09-R01: lighting_grammar contains temporal_signal
        for s in slides:
            if "temporal_signal" not in s.pssl.lighting_grammar:
                violations.append(GateC09Rule.C09_R01_LIGHTING_TEMPORAL)
                checks.append(GateC09CheckResult(
                    rule=GateC09Rule.C09_R01_LIGHTING_TEMPORAL,
                    passed=False,
                    detail=f"slide {s.slide_index} missing temporal_signal",
                ))
                break
        else:
            checks.append(GateC09CheckResult(
                rule=GateC09Rule.C09_R01_LIGHTING_TEMPORAL, passed=True,
            ))

        # C09-R02: saturation_pct numeric 0-100
        r02_ok = all(
            isinstance(s.pssl.saturation_pct, int) and 0 <= s.pssl.saturation_pct <= 100
            for s in slides
        )
        if not r02_ok:
            violations.append(GateC09Rule.C09_R02_SATURATION_NUMERIC)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R02_SATURATION_NUMERIC, passed=r02_ok,
        ))

        # C09-R03: ≥ 3 TIAR nouns on text slides (every slide is text for now)
        r03_ok = True
        for s in slides:
            if s.slide_type in ("text", "hook_cover", "tension_build", "body_text"):
                if len(s.tribal_noun_assignments) < MIN_TIAR_NOUNS_PER_TEXT_SLIDE:
                    r03_ok = False
                    break
        if not r03_ok:
            violations.append(GateC09Rule.C09_R03_TIAR_COVERAGE)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R03_TIAR_COVERAGE, passed=r03_ok,
        ))

        # C09-R04: gaze geometry numeric
        r04_ok = all(
            isinstance(s.pssl.head_rotation_degrees, (int, float))
            and isinstance(s.pssl.pupil_position_ratio_pct, (int, float))
            for s in slides
        )
        if not r04_ok:
            violations.append(GateC09Rule.C09_R04_GAZE_GEOMETRY)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R04_GAZE_GEOMETRY, passed=r04_ok,
        ))

        # C09-R05: PAD scores valid
        r05_ok = True
        for s in slides:
            pad = s.pssl.pad_environmental_grammar
            if not (-1.0 <= pad.P <= 1.0 and -1.0 <= pad.A <= 1.0 and -1.0 <= pad.D <= 1.0):
                r05_ok = False
                break
        if not r05_ok:
            violations.append(GateC09Rule.C09_R05_PAD_SCORES)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R05_PAD_SCORES, passed=r05_ok,
        ))

        # C09-R06: tension/accumulation slides have non-null artifact
        r06_ok = True
        arc = inp.somatic_arc_type
        is_artifact_arc = arc in (
            SomaticArcType.TENSION_RELEASE,
            SomaticArcType.TENSION_RELEASE.value,
            SomaticArcType.ACCUMULATION_CLIFF,
            SomaticArcType.ACCUMULATION_CLIFF.value,
        )
        if is_artifact_arc:
            for s in slides:
                # Last slide excluded (release / cliff)
                if s.slide_index < len(slides) - 1:
                    if s.pssl.incomplete_tribal_artifact is None:
                        r06_ok = False
                        break
        if not r06_ok:
            violations.append(GateC09Rule.C09_R06_INCOMPLETE_ARTIFACT)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R06_INCOMPLETE_ARTIFACT, passed=r06_ok,
        ))

        # C09-R07: semiotic injection not on slide 0 or 1 for 4+ slides
        r07_ok = True
        if semiotic is not None:
            if semiotic.injection_slide_index < 2 and semiotic.total_slides >= SEMIOTIC_INJECTION_MIN_SLIDES:
                r07_ok = False
        if not r07_ok:
            violations.append(GateC09Rule.C09_R07_SEMIOTIC_POSITION)
        checks.append(GateC09CheckResult(
            rule=GateC09Rule.C09_R07_SEMIOTIC_POSITION, passed=r07_ok,
        ))

        verdict = GateC09Verdict.PASS if not violations else GateC09Verdict.FAIL
        return GateC09Result(
            verdict=verdict,
            checks=checks,
            violations=violations,
        )

    # ================================================================== #
    # AUTO-REVISION
    # ================================================================== #

    def _auto_revise(
        self,
        slides: list[PerSlideAssignment],
        gate_result: GateC09Result,
        inp: VCBGenerationInput,
    ) -> list[PerSlideAssignment]:
        """
        Attempt to fix known violations automatically.
        Returns a revised slide list.
        """
        revised = [s.model_copy(deep=True) for s in slides]

        for v in gate_result.violations:
            if v in (GateC09Rule.C09_R01_LIGHTING_TEMPORAL, GateC09Rule.C09_R01_LIGHTING_TEMPORAL.value):
                for s in revised:
                    if "temporal_signal" not in s.pssl.lighting_grammar:
                        s.pssl = s.pssl.model_copy(
                            update={
                                "lighting_grammar": (
                                    s.pssl.lighting_grammar
                                    + ", temporal_signal: 5000K-5500K neutral hold"
                                ),
                            },
                        )

            if v in (GateC09Rule.C09_R03_TIAR_COVERAGE, GateC09Rule.C09_R03_TIAR_COVERAGE.value):
                active = [n for n in inp.active_nouns if n not in inp.blocked_nouns]
                positions = ["hook_text", "body_text", "subtext"]
                for s in revised:
                    while (
                        len(s.tribal_noun_assignments) < MIN_TIAR_NOUNS_PER_TEXT_SLIDE
                        and active
                    ):
                        j = len(s.tribal_noun_assignments)
                        noun = active[j % len(active)]
                        s.tribal_noun_assignments.append(
                            TribalNounAssignment(
                                noun=noun,
                                position=positions[j % len(positions)],
                                congruent_visual_element=f"visual congruence for '{noun}'",
                            )
                        )

            if v in (GateC09Rule.C09_R06_INCOMPLETE_ARTIFACT, GateC09Rule.C09_R06_INCOMPLETE_ARTIFACT.value):
                for s in revised:
                    if (
                        s.slide_index < len(revised) - 1
                        and s.pssl.incomplete_tribal_artifact is None
                    ):
                        s.pssl = s.pssl.model_copy(
                            update={"incomplete_tribal_artifact": "half-drawn circle"},
                        )

        return revised

    # ================================================================== #
    # CLASSIFICATION HELPERS
    # ================================================================== #

    @staticmethod
    def _classify_slide(index: int, inp: VCBGenerationInput) -> str:
        """Assign a slide_type label."""
        if index == 0:
            return "hook_cover"
        if index == inp.slide_count - 1:
            return "cta_close"
        arc = inp.somatic_arc_type
        if arc in (SomaticArcType.TENSION_RELEASE, SomaticArcType.TENSION_RELEASE.value):
            peak_idx = round(inp.slide_count * 0.6)
            if index <= peak_idx:
                return f"tension_build_{index}"
            return f"release_{index}"
        if arc in (SomaticArcType.ACCUMULATION_CLIFF, SomaticArcType.ACCUMULATION_CLIFF.value):
            return f"accumulation_{index}"
        return f"body_{index}"

    @staticmethod
    def _default_image_type(index: int, inp: VCBGenerationInput) -> str:
        if index == 0:
            return "tier_3_ai_realistic"
        return "tier_2_stock_contextual"

    # ================================================================== #
    # CLASS-LEVEL UTILITY — accumulation imagery scan
    # ================================================================== #

    @staticmethod
    def scan_completion_imagery(text: str) -> list[str]:
        """
        Return list of completion-imagery keywords found in *text*.
        Used by Stage 4 Step 7 and tests.
        """
        lower = text.lower()
        return [kw for kw in COMPLETION_IMAGERY_KEYWORDS if kw in lower]

    # ================================================================== #
    # CLASS-LEVEL UTILITY — semiotic injection validator
    # ================================================================== #

    @staticmethod
    def validate_semiotic_position(
        injection_index: int,
        total_slides: int,
    ) -> bool:
        """
        Return True if the injection index is valid per C09-R07.
        """
        if total_slides < SEMIOTIC_INJECTION_MIN_SLIDES:
            return True  # Rule doesn't apply
        return injection_index >= 2
