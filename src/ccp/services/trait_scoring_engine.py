"""
CCP FR7 Leadership Scorecard — Trait Scoring Engine (Unit 3)
Phase 2 SCORE: 12 individual trait scoring rubrics per spec signal tables.

Spec reference: FR7 Tech Spec §Phase 2: SCORE — 12 Trait Evaluation
                §Signal Sources per Trait (rubric tables for each trait)

Each trait is scored independently on a 1–10 scale using signals from the
loaded DEP objects. Evidence citations are mandatory per AC3.

Technical decisions (spec):
  - 12 traits scored independently, not composited
  - Minister of Identity is inference-time, not training-time
  - Weak traits ≠ bad traits (developmental, not evaluative)
  - Two architectural gaps are features (Devotional Passion, Comic Honesty)
"""

from typing import Any, Optional

from src.ccp.models.leadership_scorecard_models import (
    TRAIT_REGISTRY,
    TRAIT_SCORE_MAX,
    TRAIT_SCORE_MIN,
    ScoredTrait,
    TraitCategory,
    TraitEvidence,
    TraitName,
)
from src.ccp.services.signal_source_loader import SignalBundle


class TraitScoringEngine:
    """Scores all 12 leadership traits from signal bundle data.

    Spec §Phase 2 SCORE: For each of the 12 traits, the Minister evaluates
    signal evidence and assigns a score.

    Each trait scorer extracts signals from the relevant DEP objects and applies
    the rubric defined in the spec's signal/scoring tables.
    """

    def __init__(self, signal_bundle: SignalBundle):
        """Initialize with a validated signal bundle from Phase 1.

        Args:
            signal_bundle: The SignalBundle containing all loaded DEP data.
        """
        self.bundle = signal_bundle
        self._coach_soul = signal_bundle.coach_soul_data
        self._ttt_baseline = signal_bundle.ttt_baseline_data
        self._tribe_soul = signal_bundle.tribe_soul_data
        self._cmm = signal_bundle.cultural_memory_map_data
        self._story_archive = signal_bundle.coach_story_archive_data
        self._philosophy = signal_bundle.philosophy_brief_data

    def score_all_traits(self) -> list[ScoredTrait]:
        """Score all 12 traits and return the scored trait list.

        Returns:
            List of 12 ScoredTrait objects with evidence citations.
        """
        scorers = {
            TraitName.DEEP_EMPATHY: self._score_deep_empathy,
            TraitName.AUTHENTIC_VULNERABILITY: self._score_authentic_vulnerability,
            TraitName.EMBODIED_CONFIDENCE: self._score_embodied_confidence,
            TraitName.EMOTIONAL_DEPTH: self._score_emotional_depth,
            TraitName.DEVOTIONAL_PASSION: self._score_devotional_passion,
            TraitName.MYSTIQUE_AND_AURA: self._score_mystique_and_aura,
            TraitName.ARCHETYPAL_STORYTELLING: self._score_archetypal_storytelling,
            TraitName.TRANSFORMATION_PROOF: self._score_transformation_proof,
            TraitName.POLARIZING_CLARITY: self._score_polarizing_clarity,
            TraitName.EXPANSION_ENERGY: self._score_expansion_energy,
            TraitName.COMIC_HONESTY: self._score_comic_honesty,
            TraitName.DIRECTNESS: self._score_directness,
        }

        scored_traits: list[ScoredTrait] = []
        for entry in TRAIT_REGISTRY:
            trait_name: TraitName = entry["name"]
            scorer_fn = scorers[trait_name]
            raw_score, evidence = scorer_fn()

            # Clamp to bounds (AC8)
            clamped_score = max(TRAIT_SCORE_MIN, min(TRAIT_SCORE_MAX, raw_score))

            scored_traits.append(ScoredTrait(
                trait_id=entry["trait_id"],
                name=trait_name,
                label=entry["label"],
                score=clamped_score,
                category=entry["category"],
                evidence=evidence,
            ))

        return scored_traits

    # ── Helper extractors ────────────────────────────────────────

    def _safe_get(self, data: Optional[dict], *keys: str, default: Any = None) -> Any:
        """Safely navigate nested dicts."""
        current = data
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key, default)
        return current

    def _count_items(self, data: Optional[dict], *keys: str) -> int:
        """Count items in a nested list field."""
        val = self._safe_get(data, *keys, default=[])
        if isinstance(val, list):
            return len(val)
        return 0

    # ── Trait 1: Deep Empathy (1–10) ─────────────────────────────
    # Spec: L1/L2/L3 depth coverage from tribe_soul.json
    #       Audience emotional references in voice from coach_soul.json
    #       Mode coverage (T/V/R) from tribe_soul.json
    #       Empathy language markers from LIWC-22

    def _score_deep_empathy(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: L1/L2/L3 depth coverage (tribe_soul.json)
        # Rubric: L3 ≥10% → +3. L2 ≥30% → +2. L1 only → 0
        depth_dist = self._safe_get(self._tribe_soul, "depth_distribution", default={})
        l3_pct = depth_dist.get("l3_percentage", 0) if isinstance(depth_dist, dict) else 0
        l2_pct = depth_dist.get("l2_percentage", 0) if isinstance(depth_dist, dict) else 0

        if l3_pct >= 10:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"L3 depth coverage at {l3_pct}% (≥10% threshold met)",
                rubric_points=3,
            ))
        elif l2_pct >= 30:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"L2 depth coverage at {l2_pct}% (≥30% threshold met), L3 at {l3_pct}%",
                rubric_points=2,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"Depth coverage L1-dominant: L2={l2_pct}%, L3={l3_pct}%",
                rubric_points=0,
            ))

        # Signal 2: Audience emotional references in voice (coach_soul.json)
        # Rubric: ≥5 tribe-referencing emotional passages → +2
        emotional_peaks = self._safe_get(self._coach_soul, "voice_dna", "emotional_peak_markers", default=[])
        emotional_count = len(emotional_peaks) if isinstance(emotional_peaks, list) else 0
        if emotional_count >= 5:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"{emotional_count} emotional peak markers detected (≥5 threshold met)",
                rubric_points=2,
            ))

        # Signal 3: Mode coverage (T/V/R) from tribe_soul.json
        # Rubric: All 3 modes covered with ≥3 triggers each → +2
        mode_dist = self._safe_get(self._tribe_soul, "mode_distribution", default={})
        modes_covered = 0
        for mode_key in ["thought", "visceral", "reflective"]:
            mode_count = mode_dist.get(mode_key, 0) if isinstance(mode_dist, dict) else 0
            if mode_count >= 3:
                modes_covered += 1
        if modes_covered >= 3:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"All 3 T/V/R modes covered with ≥3 triggers each",
                rubric_points=2,
            ))

        # Signal 4: Empathy language markers (LIWC-22)
        # Rubric: Social referencing words above 50th percentile → +1
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        social_score = liwc.get("social", 0) if isinstance(liwc, dict) else 0
        if social_score > 50:
            score += 1
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (Sacred Audio)",
                description=f"Social referencing score {social_score} (above 50th percentile)",
                rubric_points=1,
            ))

        # Ensure at least 1 evidence item (AC3)
        if not evidence:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description="No strong empathy signals detected in signal sources",
                rubric_points=0,
            ))

        return max(1, score), evidence

    # ── Trait 2: Authentic Vulnerability (1–10) ──────────────────
    # Spec: Negative Space richness (DEP-ENG-004)
    #       Emotional charge markers (Sacred Audio)
    #       Hedging language in emotional passages (coach_soul.json)
    #       Self-referential depth (LIWC-22)

    def _score_authentic_vulnerability(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Negative Space richness (DEP-ENG-004)
        # Rubric: ≥5 documented avoidance zones → +3
        negative_space = self._safe_get(self._coach_soul, "negative_space", default={})
        avoidance_zones = self._safe_get(negative_space, "avoidance_zones", default=[])
        avoidance_count = len(avoidance_zones) if isinstance(avoidance_zones, list) else 0
        if avoidance_count >= 5:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-004 (Negative Space)",
                description=f"{avoidance_count} documented avoidance zones (≥5 threshold met)",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-004 (Negative Space)",
                description=f"{avoidance_count} avoidance zones documented (below 5 threshold)",
                rubric_points=0,
            ))

        # Signal 2: Emotional charge markers (Sacred Audio)
        # Rubric: ≥3 voice cracks/pauses/speed changes flagged → +3
        charge_markers = self._safe_get(self._coach_soul, "emotional_charge_markers", default=[])
        charge_count = len(charge_markers) if isinstance(charge_markers, list) else 0
        if charge_count >= 3:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="Sacred Audio (emotional charge)",
                description=f"{charge_count} emotional charge markers detected (≥3 threshold met)",
                rubric_points=3,
            ))

        # Signal 3: Hedging language in emotional passages
        # Rubric: Low hedging → +2 (coach doesn't soften vulnerability)
        hedging_rate = self._safe_get(self._coach_soul, "hedging_rate", default=1.0)
        if isinstance(hedging_rate, (int, float)) and hedging_rate < 0.3:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"Low hedging rate {hedging_rate:.2f} in emotional passages",
                rubric_points=2,
            ))

        # Signal 4: Self-referential depth (LIWC-22)
        # Rubric: High I-word frequency in vulnerability passages → +2
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        i_word_freq = liwc.get("i_words", 0) if isinstance(liwc, dict) else 0
        if i_word_freq > 50:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (Sacred Audio)",
                description=f"I-word frequency {i_word_freq} in vulnerability passages (above 50th percentile)",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 3: Embodied Confidence (1–10) ──────────────────────
    # Spec: TTT ceiling, TTT consistency (drift), Temperature range, Vocal authority

    def _score_embodied_confidence(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: TTT ceiling (ttt_baseline.json)
        # Rubric: TTT-08+ → +3. TTT-06/07 → +2. TTT-05 or below → +1
        ttt_ceiling = self._safe_get(self._ttt_baseline, "ttt_ceiling", default=0)
        if isinstance(ttt_ceiling, (int, float)):
            if ttt_ceiling >= 8:
                score += 3
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT ceiling at {ttt_ceiling} (≥TTT-08 threshold met)",
                    rubric_points=3,
                ))
            elif ttt_ceiling >= 6:
                score += 2
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT ceiling at {ttt_ceiling} (TTT-06/07 range)",
                    rubric_points=2,
                ))
            else:
                score += 1
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT ceiling at {ttt_ceiling} (TTT-05 or below)",
                    rubric_points=1,
                ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-005 (ttt_baseline.json)",
                description="TTT ceiling data not available",
                rubric_points=0,
            ))

        # Signal 2: TTT consistency / drift (ttt_baseline.json)
        # Rubric: Drift <10% → +3. <15% → +2. ≥15% → +1
        drift = self._safe_get(self._ttt_baseline, "drift_percentage", default=100.0)
        if isinstance(drift, (int, float)):
            if drift < 10:
                score += 3
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT drift at {drift:.1f}% (<10% threshold met)",
                    rubric_points=3,
                ))
            elif drift < 15:
                score += 2
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT drift at {drift:.1f}% (<15% threshold met)",
                    rubric_points=2,
                ))
            else:
                score += 1
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-005 (ttt_baseline.json)",
                    description=f"TTT drift at {drift:.1f}% (≥15%)",
                    rubric_points=1,
                ))

        # Signal 3: Temperature range breadth (ttt_baseline.json)
        # Rubric: Can credibly operate across ≥4 TTT levels → +2
        range_breadth = self._safe_get(self._ttt_baseline, "temperature_range_breadth", default=0)
        if isinstance(range_breadth, (int, float)) and range_breadth >= 4:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-005 (ttt_baseline.json)",
                description=f"Temperature range breadth of {range_breadth} TTT levels (≥4 threshold met)",
                rubric_points=2,
            ))

        # Signal 4: Vocal authority markers (DEP-ENG-003)
        # Rubric: Strong declarative rhythms, low uptalk → +2
        sentence_rhythm = self._safe_get(self._coach_soul, "voice_dna", "sentence_rhythm", default=[])
        rhythm_count = len(sentence_rhythm) if isinstance(sentence_rhythm, list) else 0
        if rhythm_count >= 3:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"{rhythm_count} declarative rhythm patterns detected",
                rubric_points=2,
            ))

        if not evidence:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-005 (ttt_baseline.json)",
                description="Insufficient TTT data for confidence scoring",
                rubric_points=0,
            ))

        return max(1, score), evidence

    # ── Trait 4: Emotional Depth (1–10) ──────────────────────────
    # Spec: Metaphor density, Sub-surface emotion naming, Linguistic complexity, Narrative layering

    def _score_emotional_depth(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Metaphor density (DEP-ENG-003 + DEP-ENG-004)
        # Rubric: ≥3 original metaphors in voice corpus → +3
        metaphors = self._safe_get(self._coach_soul, "voice_dna", "metaphor_patterns", default=[])
        metaphor_count = len(metaphors) if isinstance(metaphors, list) else 0
        if metaphor_count >= 3:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 + DEP-ENG-004",
                description=f"{metaphor_count} original metaphor patterns in voice corpus (≥3 threshold met)",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 + DEP-ENG-004",
                description=f"{metaphor_count} metaphor patterns detected (below 3 threshold)",
                rubric_points=0,
            ))

        # Signal 2: Sub-surface emotion naming (coach_soul.json)
        # Rubric: Names 2+ emotions beneath surface emotion → +3
        sub_emotions = self._safe_get(self._coach_soul, "sub_surface_emotions", default=[])
        sub_count = len(sub_emotions) if isinstance(sub_emotions, list) else 0
        if sub_count >= 2:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"{sub_count} sub-surface emotions named (≥2 threshold met)",
                rubric_points=3,
            ))

        # Signal 3: Linguistic complexity (LIWC-22)
        # Rubric: Cognitive complexity score above 60th percentile → +2
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        cog_complexity = liwc.get("cognitive_complexity", 0) if isinstance(liwc, dict) else 0
        if cog_complexity > 60:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (Sacred Audio)",
                description=f"Cognitive complexity score {cog_complexity} (above 60th percentile)",
                rubric_points=2,
            ))

        # Signal 4: Narrative layering (Voice DNA)
        # Rubric: Multi-layer narrative structure detected → +2
        vocab_fingerprint = self._safe_get(self._coach_soul, "voice_dna", "vocabulary_fingerprint", default=[])
        narrative_markers = [v for v in (vocab_fingerprint if isinstance(vocab_fingerprint, list) else [])
                            if isinstance(v, str) and any(kw in v.lower() for kw in ["narrative", "story", "layer", "arc"])]
        if len(narrative_markers) >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"Narrative layering markers detected in vocabulary fingerprint",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 5: Devotional Passion (1–10) ───────────────────────
    # Spec: Emotional intensity, Unprompted expansion, Sacred Audio volume, Craft discussion fire

    def _score_devotional_passion(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Emotional intensity markers (Sacred Audio)
        # Rubric: Peak emotional intensity ≥80th percentile → +3
        peak_intensity = self._safe_get(self._coach_soul, "peak_emotional_intensity", default=0)
        if isinstance(peak_intensity, (int, float)) and peak_intensity >= 80:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="Sacred Audio (emotional intensity)",
                description=f"Peak emotional intensity at {peak_intensity}th percentile (≥80th threshold met)",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="Sacred Audio (emotional intensity)",
                description=f"Peak emotional intensity at {peak_intensity} percentile",
                rubric_points=0,
            ))

        # Signal 2: Unprompted expansion (Interview corpus)
        # Rubric: Coach expands beyond question scope ≥3 times → +2
        expansion_count = self._safe_get(self._coach_soul, "unprompted_expansion_count", default=0)
        if isinstance(expansion_count, (int, float)) and expansion_count >= 3:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="Interview corpus",
                description=f"Coach expanded beyond question scope {expansion_count} times (≥3 threshold met)",
                rubric_points=2,
            ))

        # Signal 3: Sacred Audio volume
        # Rubric: Submitted words significantly exceed 3,000 minimum → +2
        word_count = self._safe_get(self._coach_soul, "total_word_count", default=0)
        if isinstance(word_count, (int, float)) and word_count > 6000:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="Sacred Audio volume",
                description=f"{word_count} words submitted (significantly exceeds 3,000 minimum)",
                rubric_points=2,
            ))

        # Signal 4: Craft discussion fire (coach_soul.json)
        # Rubric: Evidence of intrinsic motivation language → +3
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        achievement = liwc.get("achievement", 0) if isinstance(liwc, dict) else 0
        pos_emotion = liwc.get("positive_emotion", 0) if isinstance(liwc, dict) else 0
        if achievement > 50 and pos_emotion > 50:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (coach_soul.json)",
                description=f"Achievement ({achievement}) + Positive emotion ({pos_emotion}) above 50th percentile",
                rubric_points=3,
            ))

        return max(1, score), evidence

    # ── Trait 6: Mystique & Aura (1–10) ──────────────────────────
    # Spec: Content Pillar breadth, Strategic withholding, Knowledge territory ratio, Info gap creation

    def _score_mystique_and_aura(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Content Pillar breadth
        # Rubric: ≥7 content territories mapped → +3
        pillars = self._safe_get(self._coach_soul, "content_pillars", default=[])
        pillar_count = len(pillars) if isinstance(pillars, list) else 0
        if pillar_count >= 7:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="Pillar document",
                description=f"{pillar_count} content territories mapped (≥7 threshold met)",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="Pillar document",
                description=f"{pillar_count} content territories mapped (below 7 threshold)",
                rubric_points=0,
            ))

        # Signal 2: Strategic withholding (coach_soul.json)
        # Rubric: Coach implies deeper knowledge without revealing it ≥2 times → +2
        withholding_markers = self._safe_get(self._coach_soul, "strategic_withholding_markers", default=[])
        withholding_count = len(withholding_markers) if isinstance(withholding_markers, list) else 0
        if withholding_count >= 2:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"{withholding_count} strategic withholding markers detected (≥2 threshold met)",
                rubric_points=2,
            ))

        # Signal 3: Knowledge territory ratio (Pillars vs public sharing)
        # Rubric: Wide gap between known territory and revealed territory → +3
        frameworks = self._safe_get(self._coach_soul, "signature_frameworks", default=[])
        framework_count = len(frameworks) if isinstance(frameworks, list) else 0
        if framework_count >= 3 and pillar_count >= 5:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="coach_soul.json (frameworks vs. pillars)",
                description=f"{framework_count} frameworks and {pillar_count} pillars suggest knowledge depth gap",
                rubric_points=3,
            ))

        # Signal 4: Information gap creation (Voice DNA)
        # Rubric: Uses open-loop language → +2
        vocab = self._safe_get(self._coach_soul, "voice_dna", "vocabulary_fingerprint", default=[])
        open_loop_markers = [v for v in (vocab if isinstance(vocab, list) else [])
                            if isinstance(v, str) and any(kw in v.lower() for kw in
                            ["more to this", "let me focus", "another time", "deeper"])]
        if len(open_loop_markers) >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"Open-loop language patterns detected in vocabulary fingerprint",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 7: Archetypal Storytelling (1–10) ──────────────────
    # Spec: Story count (DEP-ENG-024), Hartian 5-element, Arc diversity, Narrative rhythm

    def _score_archetypal_storytelling(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Story count (DEP-ENG-024)
        # Rubric: ≥5 structured stories → +2. ≥10 → +3
        stories = self._safe_get(self._story_archive, "stories", default=[])
        story_count = len(stories) if isinstance(stories, list) else 0
        if story_count >= 10:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{story_count} structured stories in archive (≥10 threshold met)",
                rubric_points=3,
            ))
        elif story_count >= 5:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{story_count} structured stories in archive (≥5 threshold met)",
                rubric_points=2,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{story_count} stories in archive (below 5 threshold — optional source not fully populated)",
                rubric_points=0,
            ))

        # Signal 2: Hartian 5-element completion (DEP-ENG-024)
        # Rubric: All 5 elements present in ≥3 stories → +3
        hartian_complete = 0
        for story in (stories if isinstance(stories, list) else []):
            if isinstance(story, dict):
                elements = story.get("hartian_elements", {})
                if isinstance(elements, dict) and len(elements) >= 5:
                    hartian_complete += 1
        if hartian_complete >= 3:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{hartian_complete} stories with complete Hartian 5-element schema (≥3 threshold met)",
                rubric_points=3,
            ))

        # Signal 3: Arc diversity (DEP-ENG-024)
        # Rubric: Both redemption AND contamination sequences present → +2
        arc_types = set()
        for story in (stories if isinstance(stories, list) else []):
            if isinstance(story, dict):
                arc = story.get("arc_type", "")
                if arc:
                    arc_types.add(arc.lower())
        has_redemption = any("redemption" in a for a in arc_types)
        has_contamination = any("contamination" in a for a in arc_types)
        if has_redemption and has_contamination:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description="Both redemption and contamination arc sequences present",
                rubric_points=2,
            ))

        # Signal 4: Narrative rhythm (DEP-ENG-003)
        # Rubric: Natural story cadence detected in Voice DNA → +2
        rhythm = self._safe_get(self._coach_soul, "voice_dna", "sentence_rhythm", default=[])
        rhythm_count = len(rhythm) if isinstance(rhythm, list) else 0
        if rhythm_count >= 2:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"Natural story cadence detected: {rhythm_count} rhythm patterns",
                rubric_points=2,
            ))

        # Ensure at least 1 evidence for AC3
        if not evidence:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description="Story archive not available — minimal storytelling evidence",
                rubric_points=0,
            ))

        return max(1, score), evidence

    # ── Trait 8: Transformation Proof (1–10) ─────────────────────
    # Spec: Client transformation stories, Measurable outcomes, Before/after, CBCS tracking

    def _score_transformation_proof(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Client transformation stories (DEP-ENG-024)
        # Rubric: ≥2 documented client transformations with specific outcomes → +3
        stories = self._safe_get(self._story_archive, "stories", default=[])
        client_transformations = [s for s in (stories if isinstance(stories, list) else [])
                                  if isinstance(s, dict) and s.get("type") == "client_transformation"]
        if len(client_transformations) >= 2:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{len(client_transformations)} client transformation stories documented (≥2 threshold met)",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{len(client_transformations)} client transformation stories (below 2 threshold)",
                rubric_points=0,
            ))

        # Signal 2: Measurable outcomes cited (Interview corpus)
        # Rubric: Coach cites specific numbers/metrics → +3
        measurable_outcomes = self._safe_get(self._coach_soul, "measurable_outcomes", default=[])
        outcome_count = len(measurable_outcomes) if isinstance(measurable_outcomes, list) else 0
        if outcome_count >= 1:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="Interview corpus",
                description=f"{outcome_count} measurable outcomes cited with specific metrics",
                rubric_points=3,
            ))

        # Signal 3: Before/after evidence (Story Archive)
        # Rubric: ≥1 clear before/after journey → +2
        before_after = [s for s in (stories if isinstance(stories, list) else [])
                        if isinstance(s, dict) and s.get("has_before_after", False)]
        if len(before_after) >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-024 (Coach Story Archive)",
                description=f"{len(before_after)} stories with clear before/after journey",
                rubric_points=2,
            ))

        # Signal 4: CBCS tracking data (if available)
        # Rubric: Active client tracking with documented progress → +2
        cbcs_active = self._safe_get(self._coach_soul, "cbcs_tracking_active", default=False)
        if cbcs_active:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="CBCS (client tracking)",
                description="Active CBCS client tracking with documented progress",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 9: Polarizing Clarity (1–10) ───────────────────────
    # Spec: Enemy naming specificity, Definitive language, Position staking, Tribal alignment

    def _score_polarizing_clarity(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Enemy naming specificity (tribe_soul.json)
        # Rubric: Named enemies with mechanism descriptions (not abstract) → +3
        enemies = self._safe_get(self._tribe_soul, "enemies", default=[])
        named_enemies = [e for e in (enemies if isinstance(enemies, list) else [])
                         if isinstance(e, dict) and e.get("mechanism")]
        if len(named_enemies) >= 1:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"{len(named_enemies)} named enemies with mechanism descriptions",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description="No named enemies with mechanism descriptions found",
                rubric_points=0,
            ))

        # Signal 2: Definitive language (DEP-ENG-003)
        # Rubric: Low qualification markers, strong declarative style → +2
        hedging_rate = self._safe_get(self._coach_soul, "hedging_rate", default=1.0)
        if isinstance(hedging_rate, (int, float)) and hedging_rate < 0.2:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Positive Space)",
                description=f"Very low hedging rate {hedging_rate:.2f} — strong declarative style",
                rubric_points=2,
            ))

        # Signal 3: Position staking (Voice DNA)
        # Rubric: Coach takes unambiguous positions ≥3 times in corpus → +3
        positions = self._safe_get(self._coach_soul, "position_statements", default=[])
        position_count = len(positions) if isinstance(positions, list) else 0
        if position_count >= 3:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"{position_count} unambiguous positions staked in corpus (≥3 threshold met)",
                rubric_points=3,
            ))

        # Signal 4: Tribal alignment pattern (tribe_soul.json)
        # Rubric: Clear in-group/out-group boundary articulated → +2
        in_group = self._safe_get(self._tribe_soul, "in_group_markers", default=[])
        out_group = self._safe_get(self._tribe_soul, "out_group_markers", default=[])
        in_count = len(in_group) if isinstance(in_group, list) else 0
        out_count = len(out_group) if isinstance(out_group, list) else 0
        if in_count >= 1 and out_count >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-001 (tribe_soul.json)",
                description=f"Clear in-group ({in_count}) and out-group ({out_count}) boundaries articulated",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 10: Expansion Energy (1–10) ────────────────────────
    # Spec: Generosity markers, Growth vs dependency stance, Empowerment language, Teaching frame

    def _score_expansion_energy(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Generosity markers (coach_soul.json)
        # Rubric: Coach gives away key insights (not hoarding) → +3
        generosity_markers = self._safe_get(self._coach_soul, "generosity_markers", default=[])
        generosity_count = len(generosity_markers) if isinstance(generosity_markers, list) else 0
        if generosity_count >= 1:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"{generosity_count} generosity markers detected — coach gives away key insights",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description="No explicit generosity markers detected in signal sources",
                rubric_points=0,
            ))

        # Signal 2: Growth vs. dependency stance (Philosophy Brief)
        # Rubric: Explicit commitment to audience independence → +3
        if self._philosophy:
            independence_stance = self._safe_get(self._philosophy, "audience_independence_stance", default="")
            if independence_stance:
                score += 3
                evidence.append(TraitEvidence(
                    signal_source="Philosophy Brief",
                    description=f"Explicit commitment to audience independence: '{str(independence_stance)[:80]}'",
                    rubric_points=3,
                ))

        # Signal 3: Empowerment language (LIWC-22)
        # Rubric: Achievement + power language directed OUTWARD → +2
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        power_score = liwc.get("power", 0) if isinstance(liwc, dict) else 0
        achievement = liwc.get("achievement", 0) if isinstance(liwc, dict) else 0
        if power_score > 50 and achievement > 50:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (Sacred Audio)",
                description=f"Power ({power_score}) + Achievement ({achievement}) above 50th percentile — outward empowerment",
                rubric_points=2,
            ))

        # Signal 4: Teaching frame (Voice DNA)
        # Rubric: Instructional generosity — explains "how" not just "what" → +2
        vocab = self._safe_get(self._coach_soul, "voice_dna", "vocabulary_fingerprint", default=[])
        teaching_markers = [v for v in (vocab if isinstance(vocab, list) else [])
                           if isinstance(v, str) and any(kw in v.lower() for kw in
                           ["how to", "step by step", "here's how", "let me show", "the way"])]
        if len(teaching_markers) >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"Teaching frame detected: instructional generosity markers in vocabulary",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 11: Comic Honesty (1–10) ───────────────────────────
    # Spec: Humor markers, LIWC humor category, Tribe humor alignment, Strategic truth deployment
    # Note: "This is the system's weakest trait-servicing capability. Scores below 4/10 are expected."

    def _score_comic_honesty(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Humor markers in voice (coach_soul.json)
        # Rubric: Self-deprecation, ironic framing, comedic timing detected → +3
        humor_style = self._safe_get(self._coach_soul, "voice_dna", "humor_style", default=None)
        if humor_style and isinstance(humor_style, str) and humor_style.strip():
            score += 3
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description=f"Humor style detected: {humor_style}",
                rubric_points=3,
            ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (coach_soul.json)",
                description="No humor style classification detected in voice DNA (expected — architectural gap)",
                rubric_points=0,
            ))

        # Signal 2: LIWC-22 humor category (Sacred Audio)
        # Rubric: Humor word frequency above 50th percentile → +2
        liwc = self._safe_get(self._coach_soul, "liwc_scores", default={})
        humor_score = liwc.get("humor", 0) if isinstance(liwc, dict) else 0
        if humor_score > 50:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="LIWC-22 (Sacred Audio)",
                description=f"Humor category score {humor_score} (above 50th percentile)",
                rubric_points=2,
            ))

        # Signal 3: Tribe humor alignment (from FR6 tribe profile)
        # Rubric: Coach humor style matches tribe's dominant humor style → +3
        tribe_humor = self._safe_get(self._tribe_soul, "humor_profile", "dominant_style", default="")
        if humor_style and tribe_humor and isinstance(humor_style, str) and isinstance(tribe_humor, str):
            if humor_style.lower() in tribe_humor.lower() or tribe_humor.lower() in humor_style.lower():
                score += 3
                evidence.append(TraitEvidence(
                    signal_source="Tribe profile (humor DNA)",
                    description=f"Coach humor style '{humor_style}' aligns with tribe style '{tribe_humor}'",
                    rubric_points=3,
                ))

        # Signal 4: Strategic truth deployment (Voice corpus)
        # Rubric: Uses humor to deliver uncomfortable truths ≥1 time → +2
        strategic_humor = self._safe_get(self._coach_soul, "strategic_humor_deployments", default=[])
        if isinstance(strategic_humor, list) and len(strategic_humor) >= 1:
            score += 2
            evidence.append(TraitEvidence(
                signal_source="Voice corpus",
                description=f"{len(strategic_humor)} instances of humor deployed for uncomfortable truths",
                rubric_points=2,
            ))

        return max(1, score), evidence

    # ── Trait 12: Directness (1–10) ──────────────────────────────
    # Spec: Low hedging language, Sentence brevity, Chen AI-detection, TTT temperature

    def _score_directness(self) -> tuple[int, list[TraitEvidence]]:
        score = 0
        evidence: list[TraitEvidence] = []

        # Signal 1: Low hedging language (DEP-ENG-003)
        # Rubric: Absence of "sort of", "kind of", "maybe" in declarative passages → +3
        hedging_rate = self._safe_get(self._coach_soul, "hedging_rate", default=1.0)
        if isinstance(hedging_rate, (int, float)):
            if hedging_rate < 0.15:
                score += 3
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-003 (Positive Space)",
                    description=f"Very low hedging rate {hedging_rate:.2f} — direct declarative style",
                    rubric_points=3,
                ))
            else:
                evidence.append(TraitEvidence(
                    signal_source="DEP-ENG-003 (Positive Space)",
                    description=f"Hedging rate {hedging_rate:.2f} — moderate qualification present",
                    rubric_points=0,
                ))
        else:
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Positive Space)",
                description="Hedging rate data not available",
                rubric_points=0,
            ))

        # Signal 2: Sentence brevity (Voice DNA)
        # Rubric: Mean sentence length in declarative passages below corpus median → +2
        mean_sentence_length = self._safe_get(self._coach_soul, "mean_sentence_length", default=None)
        corpus_median = self._safe_get(self._coach_soul, "corpus_median_sentence_length", default=None)
        if (isinstance(mean_sentence_length, (int, float)) and
                isinstance(corpus_median, (int, float)) and
                mean_sentence_length < corpus_median):
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-003 (Voice DNA)",
                description=f"Mean sentence length {mean_sentence_length:.1f} below corpus median {corpus_median:.1f}",
                rubric_points=2,
            ))

        # Signal 3: Chen AI-detection score (FR3 validation)
        # Rubric: Low AI detection = high human directness → +3
        chen_score = self._safe_get(self._coach_soul, "chen_ai_detection_score", default=None)
        if isinstance(chen_score, (int, float)) and chen_score < 0.05:
            score += 3
            evidence.append(TraitEvidence(
                signal_source="FR3 validation (Chen AI detection)",
                description=f"Chen AI-detection score {chen_score:.3f} (low = high human directness)",
                rubric_points=3,
            ))

        # Signal 4: TTT temperature consistency (ttt_baseline.json)
        # Rubric: High-temperature coaches (TTT-07+) with consistency → +2
        ttt_ceiling = self._safe_get(self._ttt_baseline, "ttt_ceiling", default=0)
        drift = self._safe_get(self._ttt_baseline, "drift_percentage", default=100)
        if (isinstance(ttt_ceiling, (int, float)) and ttt_ceiling >= 7 and
                isinstance(drift, (int, float)) and drift < 15):
            score += 2
            evidence.append(TraitEvidence(
                signal_source="DEP-ENG-005 (ttt_baseline.json)",
                description=f"TTT ceiling {ttt_ceiling} (≥TTT-07) with {drift:.1f}% drift consistency",
                rubric_points=2,
            ))

        return max(1, score), evidence
