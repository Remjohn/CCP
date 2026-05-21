"""
ReactionScoreAdapter Service
Derives SFL-visible score summaries and anti-slop status from reaction performance inputs,
preserving legacy fallback mode.
"""

from __future__ import annotations
import re
from typing import Dict, Any, List, Optional
from src.ccp.models.reaction_engine_models import (
    ReactionScoreCard,
    ReactionVisibleScoreSummary,
    ReactionPerceptualScore,
    ReactionVisibleScoreName,
    ReactionPerceptualVerdict,
    ReactionVisibleMetricEvidence,
    ReactionPresenceSignal,
    ReactionSlopRiskState,
    ReactionSlopClass,
)


class ReactionScoreAdapter:
    """Adapts raw reaction scorecard metrics, acoustic signals, and transcripts into SFL-visible score language."""

    @staticmethod
    def derive_scores(
        scorecard: ReactionScoreCard,
        transcript_text: Optional[str] = None,
        acoustic_features: Optional[Dict[str, Any]] = None,
        legacy_mode: bool = False
    ) -> Optional[ReactionVisibleScoreSummary]:
        """Derives a ReactionVisibleScoreSummary from metrics and evidence.
        Returns None in legacy fallback mode (Mode B) when SFL features are disabled.
        """
        if legacy_mode or not transcript_text:
            return None

        # 1. Parse acoustic features
        acoustic = acoustic_features or {}
        conviction_density = float(acoustic.get("conviction_density", scorecard.conviction_score * 100.0))
        pacing_score = float(acoustic.get("pacing_score", 70.0))
        pause_weight = float(acoustic.get("pause_weight_score", 0.5))
        stance_force = float(acoustic.get("stance_force_score", scorecard.anti_centroid_charge))

        # 2. Transcripts Analysis
        text_lower = transcript_text.lower()
        
        # Hedge words counting
        hedges = ["probably", "maybe", "sort of", "kind of", "perhaps", "i think", "just", "mostly", "usually", "potentially"]
        hedge_count = sum(1 for h in hedges if h in text_lower)
        hedge_rate = min(1.0, hedge_count / max(1, len(transcript_text.split()) // 10))
        hedge_pressure = 1.0 - hedge_rate

        # Abstract universals
        universals = ["always", "never", "everyone", "nobody", "everything", "nothing", "all the time", "should just"]
        universal_count = sum(1 for u in universals if u in text_lower)

        # Lived specificity (numbers, dates, proper nouns)
        proper_nouns = 0
        sentences = re.split(r'[.!?]\s+', transcript_text)
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            caps = re.findall(r'\b[A-Z][a-z]{2,}\b', s)
            first_word_match = re.match(r'^([A-Z][a-z]{2,})\b', s)
            if first_word_match:
                proper_nouns += max(0, len(caps) - 1)
            else:
                proper_nouns += len(caps)
            
        numerals = len(re.findall(r"\b\d+\b", transcript_text))
        quotes = text_lower.count('"') + text_lower.count("'")
        specificity_score = min(1.0, (proper_nouns * 0.3 + numerals * 0.2 + quotes * 0.3))

        # 3. Calculate Presence Signal
        # presence_score: combines conviction density, stable pacing, pause control, and low hedging
        raw_presence = (conviction_density * 0.4 + pacing_score * 0.3 + (pause_weight * 100) * 0.15 + (hedge_pressure * 100) * 0.15)
        presence_score_int = int(max(0, min(99, raw_presence)))

        # 4. Calculate Slop Risk State
        # centroid safety: low anti-centroid score + high hedging
        centroid_collapse = (scorecard.anti_centroid_charge < 0.60 or hedge_rate > 0.4)
        # synthetic smoothness: high pacing, high conviction, but zero specificity
        synthetic_smoothness = (pacing_score > 85.0 and conviction_density > 85.0 and specificity_score < 0.1)
        # false force: high conviction but extremely high hedging or low proof
        false_force = (conviction_density > 80.0 and (hedge_rate > 0.3 or specificity_score < 0.15))
        # dead polish: high pacing, high score, but zero quotes/specificity and low anti-centroid
        dead_polish = (pacing_score > 80.0 and specificity_score == 0.0 and scorecard.anti_centroid_charge < 0.65)

        overall_slop_risk = 0
        slop_class = ReactionSlopClass.NONE

        if centroid_collapse:
            overall_slop_risk = max(overall_slop_risk, 65)
            slop_class = ReactionSlopClass.CENTROID_SAFETY
        elif false_force:
            overall_slop_risk = max(overall_slop_risk, 55)
            slop_class = ReactionSlopClass.HOLLOW_HEAT
        elif synthetic_smoothness:
            overall_slop_risk = max(overall_slop_risk, 50)
            slop_class = ReactionSlopClass.SYNTHETIC_FORCE
        elif dead_polish:
            overall_slop_risk = max(overall_slop_risk, 45)
            slop_class = ReactionSlopClass.DEAD_POLISH

        # Ensure risk stays within 0-99 bounds
        slop_risk_score = int(max(0, min(99, overall_slop_risk)))

        # 5. Derivation of 7 score families

        # --- Humanity ---
        humanity_score = int(max(0, min(99, (specificity_score * 70.0 + (1.0 - hedge_rate) * 30.0))))
        humanity_evidence = [
            ReactionVisibleMetricEvidence(metric_id="SPEC-PN", summary="Proper nouns", source_signal="proper_nouns", source_value=float(proper_nouns), contribution=0.4),
            ReactionVisibleMetricEvidence(metric_id="SPEC-NUM", summary="Numeric grounding", source_signal="numerals", source_value=float(numerals), contribution=0.3),
        ]
        humanity = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.HUMANITY,
            score_0_99=humanity_score,
            verdict=ReactionScoreAdapter._verdict_for(humanity_score),
            rationale="Authentic human texture evaluated via specificity and lack of generic structuring." if humanity_score >= 60 else "Take is generic, lacking specific named proof or dates.",
            evidence=humanity_evidence
        )

        # --- Presence ---
        presence_evidence = [
            ReactionVisibleMetricEvidence(metric_id="PRES-CONV", summary="Conviction density", source_signal="conviction_density", source_value=conviction_density, contribution=0.5),
            ReactionVisibleMetricEvidence(metric_id="PRES-HDG", summary="Hedge resistance", source_signal="hedge_rate", source_value=hedge_rate, contribution=-0.3),
        ]
        presence = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.PRESENCE,
            score_0_99=presence_score_int,
            verdict=ReactionScoreAdapter._verdict_for(presence_score_int),
            rationale="Spoken pressure stability and conviction level." if presence_score_int >= 70 else "Weak speaker conviction or excessive conversational hedging.",
            evidence=presence_evidence
        )

        # --- Trust ---
        # trust: lowered by slop risk, raised by specificity and core conviction
        trust_score = int(max(0, min(99, (specificity_score * 50.0 + (1.0 - hedge_rate) * 50.0) * (1.0 - slop_risk_score / 150.0))))
        trust = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.TRUST,
            score_0_99=trust_score,
            verdict=ReactionScoreAdapter._verdict_for(trust_score),
            rationale="Grounded credibility based on evidence and specific detail." if trust_score >= 70 else "Credibility is compromised by lack of specific proof or high slop risk.",
            evidence=[
                ReactionVisibleMetricEvidence(metric_id="TRST-SLP", summary="Slop index influence", source_signal="slop_risk_score", source_value=float(slop_risk_score), contribution=-0.5)
            ]
        )

        # --- Memorability ---
        # memorability: presence of unique words, numbers, high stance
        memo_score = int(max(0, min(99, (specificity_score * 40.0 + stance_force * 60.0))))
        memorability = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.MEMORABILITY,
            score_0_99=memo_score,
            verdict=ReactionScoreAdapter._verdict_for(memo_score),
            rationale="Presence of distinct anchors and structural contrast." if memo_score >= 60 else "Take is bland and easily forgotten.",
            evidence=[]
        )

        # --- Resonance ---
        # resonance: spoken force under pressure
        res_score = int(max(0, min(99, (raw_presence * 0.7 + stance_force * 30.0))))
        resonance = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.RESONANCE,
            score_0_99=res_score,
            verdict=ReactionScoreAdapter._verdict_for(res_score),
            rationale="Acoustic subtext and delivery pressure.",
            evidence=[]
        )

        # --- Signal ---
        # signal: anti-centroid charge minus abstract universals
        sig_score = int(max(0, min(99, (stance_force * 100.0 - universal_count * 5.0))))
        signal = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.SIGNAL,
            score_0_99=sig_score,
            verdict=ReactionScoreAdapter._verdict_for(sig_score),
            rationale="Clear worldview signature and non-centroid positioning." if sig_score >= 65 else "Weak stance clarity, sliding towards average market opinion.",
            evidence=[]
        )

        # --- AI Slop Risk ---
        ai_slop_verdict = ReactionPerceptualVerdict.STRONG if slop_risk_score < 40 else (
            ReactionPerceptualVerdict.UNSTABLE if slop_risk_score < 60 else ReactionPerceptualVerdict.BLOCKING
        )
        ai_slop_risk = ReactionPerceptualScore(
            score_name=ReactionVisibleScoreName.AI_SLOP_RISK,
            score_0_99=slop_risk_score,
            verdict=ai_slop_verdict,
            rationale=f"Risk of synthetic phrasing or empty polish: Class={slop_class.value}",
            evidence=[
                ReactionVisibleMetricEvidence(metric_id="SLP-CLASS", summary="Slop classification", source_signal="slop_class", source_value=float(len(slop_class.value)), contribution=1.0)
            ]
        )

        # Determine strengths and weaknesses
        strengths = []
        weaknesses = []

        if humanity_score >= 70:
            strengths.append("High specificity and lived texture")
        elif humanity_score < 50:
            weaknesses.append("Generic phrasing lacking concrete reference")

        if presence_score_int >= 75:
            strengths.append("Strong conviction and delivery stability")
        elif presence_score_int < 55:
            weaknesses.append("Frequent conversational hedging")

        if sig_score >= 70:
            strengths.append("Sharp non-centroid stance")
        elif sig_score < 55:
            weaknesses.append("Sliding towards market consensus")

        if slop_risk_score >= 50:
            weaknesses.append(f"AI slop signature detected: {slop_class.value}")

        return ReactionVisibleScoreSummary(
            humanity=humanity,
            presence=presence,
            trust=trust,
            memorability=memorability,
            resonance=resonance,
            signal=signal,
            ai_slop_risk=ai_slop_risk,
            top_strengths=strengths,
            top_weaknesses=weaknesses,
        )

    @staticmethod
    def derive_presence_signal(
        scorecard: ReactionScoreCard,
        acoustic_features: Optional[Dict[str, Any]] = None,
        transcript_text: Optional[str] = None
    ) -> ReactionPresenceSignal:
        """Helper to create a ReactionPresenceSignal explicitly."""
        acoustic = acoustic_features or {}
        conviction_density = float(acoustic.get("conviction_density", scorecard.conviction_score * 100.0))
        pacing_score = float(acoustic.get("pacing_score", 70.0))
        pause_weight = float(acoustic.get("pause_weight_score", 0.5))
        stance_force = float(acoustic.get("stance_force_score", scorecard.anti_centroid_charge))

        # Hedge words counting
        text_lower = (transcript_text or "").lower()
        hedges = ["probably", "maybe", "sort of", "kind of", "perhaps", "i think", "just", "mostly", "usually"]
        hedge_count = sum(1 for h in hedges if h in text_lower)
        hedge_rate = min(1.0, hedge_count / max(1, len(text_lower.split()) // 10))
        hedge_pressure = 1.0 - hedge_rate

        raw_presence = (conviction_density * 0.4 + pacing_score * 0.3 + (pause_weight * 100) * 0.15 + (hedge_pressure * 100) * 0.15)
        presence_score_int = int(max(0, min(99, raw_presence)))

        interpretation = "Speaker presence is grounded and authentic." if presence_score_int >= 70 else (
            "Speaker shows delivery instability, high hedging, or flat energy."
        )

        return ReactionPresenceSignal(
            presence_score_0_99=presence_score_int,
            conviction_density=conviction_density,
            pacing_score=pacing_score,
            pause_weight_score=pause_weight,
            stance_force_score=stance_force,
            hedge_pressure_score=hedge_pressure,
            interpretation=interpretation
        )

    @staticmethod
    def derive_slop_risk(
        scorecard: ReactionScoreCard,
        transcript_text: Optional[str] = None,
        acoustic_features: Optional[Dict[str, Any]] = None
    ) -> ReactionSlopRiskState:
        """Helper to construct a ReactionSlopRiskState explicitly."""
        text_lower = (transcript_text or "").lower()
        acoustic = acoustic_features or {}
        
        # Parse signals
        pacing_score = float(acoustic.get("pacing_score", 70.0))
        conviction_density = float(acoustic.get("conviction_density", scorecard.conviction_score * 100.0))
        
        hedges = ["probably", "maybe", "sort of", "kind of", "perhaps", "i think", "just", "mostly"]
        hedge_count = sum(1 for h in hedges if h in text_lower)
        hedge_rate = min(1.0, hedge_count / max(1, len(text_lower.split()) // 10))

        # Check specificity
        text_source = transcript_text or ""
        proper_nouns = 0
        sentences = re.split(r'[.!?]\s+', text_source)
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            caps = re.findall(r'\b[A-Z][a-z]{2,}\b', s)
            first_word_match = re.match(r'^([A-Z][a-z]{2,})\b', s)
            if first_word_match:
                proper_nouns += max(0, len(caps) - 1)
            else:
                proper_nouns += len(caps)
            
        numerals = len(re.findall(r"\b\d+\b", text_source))
        quotes = text_source.lower().count('"') + text_source.lower().count("'")
        specificity_score = min(1.0, (proper_nouns * 0.3 + numerals * 0.2 + quotes * 0.3))

        centroid_collapse = (scorecard.anti_centroid_charge < 0.60 or hedge_rate > 0.4)
        synthetic_smoothness = (pacing_score > 85.0 and conviction_density > 85.0 and specificity_score < 0.1)
        false_force = (conviction_density > 80.0 and (hedge_rate > 0.3 or specificity_score < 0.15))
        dead_polish = (pacing_score > 80.0 and specificity_score == 0.0 and scorecard.anti_centroid_charge < 0.65)

        overall_slop_risk = 0
        slop_class = ReactionSlopClass.NONE
        correction = "No immediate slop risk detected."

        if centroid_collapse:
            overall_slop_risk = 65
            slop_class = ReactionSlopClass.CENTROID_SAFETY
            correction = "Stance is too hedged or balanced. Take a clear side."
        elif false_force:
            overall_slop_risk = 55
            slop_class = ReactionSlopClass.HOLLOW_HEAT
            correction = "Acoustic force is high but lacks grounding. Add specific proof."
        elif synthetic_smoothness:
            overall_slop_risk = 50
            slop_class = ReactionSlopClass.SYNTHETIC_FORCE
            correction = "Delivery is extremely smooth but lacks human texture or concrete examples."
        elif dead_polish:
            overall_slop_risk = 45
            slop_class = ReactionSlopClass.DEAD_POLISH
            correction = "Take is clean but lacks dynamic resonance. Inject emotional subtext or pressure."

        return ReactionSlopRiskState(
            overall_risk_score_0_99=int(overall_slop_risk),
            slop_class=slop_class,
            centroid_collapse_detected=centroid_collapse,
            synthetic_smoothness_detected=synthetic_smoothness,
            false_force_detected=false_force,
            dead_polish_detected=dead_polish,
            required_correction=correction
        )

    @staticmethod
    def _verdict_for(score: int) -> ReactionPerceptualVerdict:
        if score >= 75:
            return ReactionPerceptualVerdict.STRONG
        elif score >= 55:
            return ReactionPerceptualVerdict.UNSTABLE
        elif score >= 40:
            return ReactionPerceptualVerdict.WEAK
        return ReactionPerceptualVerdict.BLOCKING
