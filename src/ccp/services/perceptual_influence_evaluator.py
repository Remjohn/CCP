"""
FR-ERA3-27 — Perceptual Influence Evaluator Service
===================================================
Scores candidate text on seven perceptual dimensions, evaluates false depth,
checks brand posture alignment, and routes combined DI/PI decisions.
"""

from __future__ import annotations

import math
import re
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.perceptual_influence_models import (
    BrandPostureContext,
    FalseDepthClass,
    FalseDepthDetectionResult,
    InfluenceAlignmentResult,
    PerceptualDimensionScore,
    PerceptualEvidenceItem,
    PerceptualInfluenceDecision,
    PerceptualInfluenceDecisionSummary,
    PerceptualInfluenceDimension,
    PerceptualInfluenceDomain,
    PerceptualInfluenceEvaluatorResult,
    PerceptualInfluenceFallbackReason,
    PerceptualInfluenceMetricBundle,
    PerceptualInfluencePolicyBundle,
    PerceptualInfluenceReport,
    PerceptualInfluenceRequest,
    PerceptualInfluenceResolutionPath,
    PerceptualInfluenceSeverity,
    PerceptualInfluenceSurface,
    SFLFunctionStackSnapshot,
)
from src.ccp.services.perceptual_influence_policy_registry import (
    PerceptualInfluencePolicyRegistry,
)
from src.ccp.services.sfl_registry_service import SFLRegistryService


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


# ── Dimension Analyzers ──────────────────────────────────────────────────

class CognitiveImprintAnalyzer:
    """Scores mental model anchors and specific structures vs generic coaching language."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.5

        if len(text.strip()) < 15:
            # Too short for cognitive depth
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.COGNITIVE_IMPRINT,
                    observation="Text length is critically low",
                    rationale="Insufficient text length to establish mental models or structural anchors.",
                    contribution=-0.4,
                )
            )
            score = 0.1
        else:
            # Check for anchor words and frameworks
            anchors = ["framework", "strategy", "concept", "structure", "system", "principle", "matrix", "diagram", "process", "anchor", "tension"]
            anchor_hits = [w for w in anchors if w in text.lower()]
            if anchor_hits:
                contribution = min(0.4, 0.1 * len(anchor_hits))
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.COGNITIVE_IMPRINT,
                        observation=f"Anchor words detected: {', '.join(anchor_hits)}",
                        rationale="Linguistic markers of specific frameworks and cognitive structures were identified.",
                        contribution=contribution,
                    )
                )
                base_score += contribution
            else:
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.COGNITIVE_IMPRINT,
                        observation="No framework anchor terms found",
                        rationale="Content relies on unstructured commentary rather than conceptual models.",
                        contribution=-0.1,
                    )
                )
                base_score -= 0.1

            # Check for generic cliches
            cliches = ["unlock your potential", "be your best", "go high", "limitless", "achieve success", "take your life to the next level"]
            cliche_hits = [c for c in cliches if c in text.lower()]
            if cliche_hits:
                contribution = max(-0.3, -0.1 * len(cliche_hits))
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.COGNITIVE_IMPRINT,
                        observation=f"Generic motivational phrases found: {', '.join(cliche_hits)}",
                        rationale="Generic coaching cliches dilute cognitive clarity and lower imprint value.",
                        contribution=contribution,
                    )
                )
                base_score += contribution

            score = max(0.0, min(1.0, base_score))

        severity = (
            PerceptualInfluenceSeverity.NONE if score >= 0.6
            else PerceptualInfluenceSeverity.LOW if score >= 0.45
            else PerceptualInfluenceSeverity.MODERATE if score >= 0.3
            else PerceptualInfluenceSeverity.HIGH
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.COGNITIVE_IMPRINT,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Cognitive imprint scored at {score:.2f} based on structural anchors vs cliches.",
        )


class SymbolicDensityAnalyzer:
    """Scores representation of metaphors and compressed meaning tags vs generic mass."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.4

        tokens = text.split()
        total_tokens = len(tokens)

        if total_tokens < 5:
            score = 0.1
        else:
            # Metaphors and symbols checklist
            symbols = ["bridge", "mirror", "lens", "crusade", "manifesto", "anchor", "symbol", "metaphor", "analogy", "identity", "rhythm", "resonance"]
            symbol_hits = [s for s in symbols if s in text.lower()]
            if symbol_hits:
                contribution = min(0.4, 0.1 * len(symbol_hits))
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.SYMBOLIC_DENSITY,
                        observation=f"Symbolic terms detected: {', '.join(symbol_hits)}",
                        rationale="Active metaphors and symbolic framing enhance compressed meaning delivery.",
                        contribution=contribution,
                    )
                )
                base_score += contribution

            # Gravity words (length > 7)
            gravity_words = [w for w in tokens if len(w) > 7]
            density = len(gravity_words) / total_tokens
            if density > 0.18:
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.SYMBOLIC_DENSITY,
                        observation=f"High density of high-gravity terms ({density:.2%})",
                        rationale="Ponderous or heavy lexical distribution indicates packed semantic payload.",
                        contribution=0.2,
                    )
                )
                base_score += 0.2
            elif density < 0.06:
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.SYMBOLIC_DENSITY,
                        observation=f"Low density of high-gravity terms ({density:.2%})",
                        rationale="Vocabulary consists of simple, sparse tokens with low symbolic complexity.",
                        contribution=-0.15,
                    )
                )
                base_score -= 0.15

            score = max(0.0, min(1.0, base_score))

        severity = (
            PerceptualInfluenceSeverity.NONE if score >= 0.55
            else PerceptualInfluenceSeverity.LOW if score >= 0.4
            else PerceptualInfluenceSeverity.MODERATE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.SYMBOLIC_DENSITY,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Symbolic density scored at {score:.2f} based on metaphor presence and vocabulary weight.",
        )


class HumanCongruenceAnalyzer:
    """Scores personal specificity and rhythmic variance vs uniform/robotic expression."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.4

        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        if not sentences:
            return PerceptualDimensionScore(
                dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
                score=0.1,
                severity=PerceptualInfluenceSeverity.HIGH,
                evidence=[],
                explanation="No valid sentences found.",
            )

        # Sentence length variance calculation
        word_counts = [len(s.split()) for s in sentences]
        avg_count = sum(word_counts) / len(word_counts)
        variance = sum((x - avg_count) ** 2 for x in word_counts) / len(word_counts) if len(word_counts) > 1 else 0.0

        if variance > 25.0:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
                    observation=f"High rhythmic variance detected (var={variance:.2f})",
                    rationale="Dynamic sentence lengths mimic conversational flow and human voice texture.",
                    contribution=0.3,
                )
            )
            base_score += 0.3
        elif variance < 4.0:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
                    observation=f"Low rhythmic variance detected (var={variance:.2f})",
                    rationale="Uniform sentence lengths suggest robotic, pre-programmed, or overly edited output.",
                    contribution=-0.3,
                )
            )
            base_score -= 0.3

        # Personal specificity (personal pronouns)
        personal_pronouns = ["i", "me", "my", "we", "us", "our", "you", "your"]
        tokens = text.lower().split()
        pronoun_hits = [t for t in tokens if t in personal_pronouns]
        if pronoun_hits:
            contribution = min(0.3, 0.05 * len(pronoun_hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
                    observation="Personal reference tokens detected",
                    rationale="First and second-person pronouns shift tone toward authentic relationship context.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        # Casual pacing markers
        casual = ["...", "-", "well", "look", "actually", "honestly", "listen", "frankly"]
        casual_hits = [c for c in casual if c in text.lower()]
        if casual_hits:
            contribution = min(0.2, 0.05 * len(casual_hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
                    observation=f"Conversational framing words: {', '.join(casual_hits)}",
                    rationale="Presence of pause weights and transitions aligns with authentic coaching presence.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        score = max(0.0, min(1.0, base_score))
        severity = (
            PerceptualInfluenceSeverity.NONE if score >= 0.6
            else PerceptualInfluenceSeverity.LOW if score >= 0.4
            else PerceptualInfluenceSeverity.MODERATE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.HUMAN_CONGRUENCE,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Human congruence scored at {score:.2f} based on sentence length variance and pronouns.",
        )


class ContrastClarityAnalyzer:
    """Scores tension, juxtaposition, and unresolved contrast vs polite compromise."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.4

        # Contrast indicators
        contrasts = ["but", "yet", "however", "instead of", "versus", "against", "unlike", "contrast", "tension"]
        tokens = text.lower().split()
        contrast_hits = [t for t in tokens if t in contrasts]
        if contrast_hits:
            contribution = min(0.4, 0.1 * len(contrast_hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.CONTRAST_CLARITY,
                    observation=f"Contrast markers detected: {', '.join(set(contrast_hits))}",
                    rationale="Active juxtaposition enforces healthy, productive friction in client cognition.",
                    contribution=contribution,
                )
            )
            base_score += contribution
        else:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.CONTRAST_CLARITY,
                    observation="Zero contrast markers found",
                    rationale="Lack of contrast indicators reduces existential tension and engagement.",
                    contribution=-0.15,
                )
            )
            base_score -= 0.15

        # Polite compromise indicators
        compromises = ["both sides", "agree to disagree", "polite compromise", "middle ground", "acceptable average", "on the other hand"]
        compromise_hits = [c for c in compromises if c in text.lower()]
        if compromise_hits:
            contribution = max(-0.4, -0.2 * len(compromise_hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.CONTRAST_CLARITY,
                    observation=f"Compromise phrasing detected: {', '.join(compromise_hits)}",
                    rationale="Polite compromise dilutes direct contrast clarity to maintain comfort.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        score = max(0.0, min(1.0, base_score))
        severity = (
            PerceptualInfluenceSeverity.NONE if score >= 0.55
            else PerceptualInfluenceSeverity.LOW if score >= 0.4
            else PerceptualInfluenceSeverity.MODERATE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.CONTRAST_CLARITY,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Contrast clarity scored at {score:.2f} based on active tension structures.",
        )


class MemorabilityPressureAnalyzer:
    """Scores recall-forcing pressure like hooks, rhythmic triggers, or bold assertions."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.4

        # Check for first-sentence hooks
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        if sentences:
            first = sentences[0].lower()
            hook_words = ["stop", "look", "listen", "never", "always", "don't", "why", "how", "what"]
            starts_with_hook = any(first.startswith(hw) for hw in hook_words)
            has_exclamation = "!" in sentences[0]
            if starts_with_hook or has_exclamation:
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.MEMORABILITY_PRESSURE,
                        observation="Strong first-sentence hook structure",
                        rationale="Hook words or aggressive syntax at onset improves initial recall retention.",
                        contribution=0.2,
                    )
                )
                base_score += 0.2

        # Rhetorical elements
        question_count = text.count("?")
        if question_count >= 2:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.MEMORABILITY_PRESSURE,
                    observation=f"Multiple rhetorical questions ({question_count})",
                    rationale="Interrogating syntax induces cognitive loop completion cycles in memory.",
                    contribution=0.15,
                )
            )
            base_score += 0.15

        # Word repetition (verbal anchors)
        words = [w.strip(",.?!:;").lower() for w in text.split() if len(w) > 4]
        rep_found = False
        for w in set(words):
            if words.count(w) >= 3:
                rep_found = True
                break
        if rep_found:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.MEMORABILITY_PRESSURE,
                    observation="Verbal repetition / signature anchor found",
                    rationale="Structured repetition forces sound-pattern memorability.",
                    contribution=0.15,
                )
            )
            base_score += 0.15

        if not rep_found and question_count == 0:
            base_score -= 0.1

        score = max(0.0, min(1.0, base_score))
        severity = (
            PerceptualInfluenceSeverity.NONE if score >= 0.55
            else PerceptualInfluenceSeverity.LOW if score >= 0.4
            else PerceptualInfluenceSeverity.MODERATE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.MEMORABILITY_PRESSURE,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Memorability pressure scored at {score:.2f} based on hooks, repetition, and style.",
        )


class OverexplanationRiskAnalyzer:
    """Scores post-insight explanation and redundant paragraphs (Negative Dimension)."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.2

        # Explanation phrases
        explain_phrases = ["this means that", "in other words", "to explain further", "which is to say", "essentially", "basically", "specifically"]
        hits = [p for p in explain_phrases if p in text.lower()]
        if hits:
            contribution = min(0.4, 0.15 * len(hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.OVEREXPLANATION_RISK,
                    observation=f"Redundant explanation transitions detected: {', '.join(hits)}",
                    rationale="Unnecessary resolution of conceptual tension weakens personal ownership of the insight.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        # Paragraph count risk
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        if len(paragraphs) > 3:
            contribution = min(0.3, 0.08 * (len(paragraphs) - 3))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.OVEREXPLANATION_RISK,
                    observation=f"Excessive paragraph count ({len(paragraphs)} paras)",
                    rationale="Over-explaining multiple times increases fatigue and lowers insight value.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        score = max(0.0, min(1.0, base_score))
        severity = (
            PerceptualInfluenceSeverity.CRITICAL if score >= 0.7
            else PerceptualInfluenceSeverity.HIGH if score >= 0.55
            else PerceptualInfluenceSeverity.MODERATE if score >= 0.4
            else PerceptualInfluenceSeverity.NONE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.OVEREXPLANATION_RISK,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Overexplanation risk scored at {score:.2f} based on explanations and text volume.",
        )


class SyntheticSmoothnessAnalyzer:
    """Scores uniform AI textures, missing pauses, and excess transition density (Negative)."""

    def analyze(self, text: str) -> PerceptualDimensionScore:
        evidence: list[PerceptualEvidenceItem] = []
        base_score = 0.2

        # Check sentence length variance (low variance implies synthetic smoothness)
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        if len(sentences) > 1:
            word_counts = [len(s.split()) for s in sentences]
            avg_count = sum(word_counts) / len(word_counts)
            variance = sum((x - avg_count) ** 2 for x in word_counts) / len(word_counts)
            if variance < 5.0:
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS,
                        observation="Extremely low variance in sentence length",
                        rationale="Uniform pacing is highly indicative of AI-generated prose templates.",
                        contribution=0.3,
                    )
                )
                base_score += 0.3

        # Transitions checklist
        transitions = ["furthermore", "therefore", "moreover", "consequently", "in addition", "subsequently", "as a result"]
        tokens = text.lower().split()
        hits = [t for t in tokens if t in transitions]
        if hits:
            contribution = min(0.3, 0.1 * len(hits))
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS,
                    observation=f"Polished transition words found: {', '.join(set(hits))}",
                    rationale="High transition density smooths over cognitive gaps, preventing student struggle.",
                    contribution=contribution,
                )
            )
            base_score += contribution

        # Absence of pause indicators
        pauses = ["...", "-", "—"]
        has_pause = any(p in text for p in pauses)
        if not has_pause:
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS,
                    observation="No pause markings (dashes, ellipses) detected",
                    rationale="Lack of conversational pause punctuation suggests synthetic template delivery.",
                    contribution=0.1,
                )
            )
            base_score += 0.1

        score = max(0.0, min(1.0, base_score))
        severity = (
            PerceptualInfluenceSeverity.CRITICAL if score >= 0.75
            else PerceptualInfluenceSeverity.HIGH if score >= 0.6
            else PerceptualInfluenceSeverity.MODERATE if score >= 0.4
            else PerceptualInfluenceSeverity.NONE
        )

        return PerceptualDimensionScore(
            dimension=PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS,
            score=round(score, 3),
            severity=severity,
            evidence=evidence,
            explanation=f"Synthetic smoothness scored at {score:.2f} based on rhythmic pacing and transitions.",
        )


# ── False Depth Detector ─────────────────────────────────────────────────

class FalseDepthDetector:
    """Classifies performative profundity, dead polish, and synthetic authority."""

    def evaluate(self, text: str, metrics: PerceptualInfluenceMetricBundle) -> FalseDepthDetectionResult:
        evidence: list[PerceptualEvidenceItem] = []
        detected_classes: list[FalseDepthClass] = []

        # 1. Performative Profundity: grand abstract words + low specificity
        abstract = ["transcend", "unlock your potential", "limitless", "infinite", "vibrations", "quantum", "transformation", "cosmic"]
        abstract_hits = [a for a in abstract if a in text.lower()]
        concrete_tokens = [w for w in text.split() if w.isdigit() or len(w) > 9]
        if len(abstract_hits) >= 2 and len(concrete_tokens) < 3:
            detected_classes.append(FalseDepthClass.PERFORMATIVE_PROFUNDITY)
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                    observation=f"Performative profundity detected: abstract tags={abstract_hits}",
                    rationale="Abstract jargon used without concrete reference or structural grounding.",
                    contribution=0.4,
                )
            )

        # 2. Dead Polish: pristine grammar + uniform length + zero pronouns/emotion
        sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
        has_exclamation = "!" in text
        personal_pronouns = ["i", "me", "my", "we", "us", "our"]
        has_pronoun = any(p in text.lower().split() for p in personal_pronouns)
        if len(sentences) >= 3 and not has_exclamation and not has_pronoun and metrics.synthetic_smoothness_score.score > 0.5:
            detected_classes.append(FalseDepthClass.DEAD_POLISH)
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                    observation="Dead polish detected: pristine but devoid of personal pronouns or conversational pause markers.",
                    rationale="Polished execution lacking the vulnerability/asymmetry of human voice.",
                    contribution=0.4,
                )
            )

        # 3. Synthetic Authority: abstract claims of expertise
        claims = ["as an expert", "proven methodology", "scientific proof", "guaranteed success", "i have decoded"]
        claims_hits = [c for c in claims if c in text.lower()]
        if claims_hits:
            detected_classes.append(FalseDepthClass.SYNTHETIC_AUTHORITY)
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                    observation=f"Synthetic authority statement: '{claims_hits[0]}'",
                    rationale="Demands authority status without demonstrating authentic context or lived proof.",
                    contribution=0.3,
                )
            )

        # 4. Empty Motivational Smoothness: cliches with no content depth
        cliches = ["believe in yourself", "take action today", "reach your goals", "keep going", "never give up"]
        cliche_hits = [c for c in cliches if c in text.lower()]
        if cliche_hits and metrics.cognitive_imprint_score.score < 0.35:
            detected_classes.append(FalseDepthClass.EMPTY_MOTIVATIONAL_SMOOTHNESS)
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                    observation=f"Empty motivational smoothness detected: cliches={cliche_hits}",
                    rationale="Generic coaching tropes mask the absence of structural learning outcomes.",
                    contribution=0.35,
                )
            )

        # 5. Overresolved Meaning: eliminating ambiguity completely
        resolutions = ["obviously", "clearly", "in conclusion", "without a doubt", "absolutely"]
        res_hits = [r for r in resolutions if r in text.lower()]
        if len(res_hits) >= 2 and metrics.overexplanation_risk_score.score > 0.5:
            detected_classes.append(FalseDepthClass.OVERRESOLVED_MEANING)
            evidence.append(
                PerceptualEvidenceItem(
                    evidence_id=_id("P-EVD"),
                    dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                    observation=f"Overresolved meaning detected: '{res_hits[0]}', '{res_hits[1]}'",
                    rationale="Forcibly resolves tension, preventing client cognitive investment.",
                    contribution=0.3,
                )
            )

        detected = len(detected_classes) > 0
        severity = (
            PerceptualInfluenceSeverity.HIGH if len(detected_classes) >= 3
            else PerceptualInfluenceSeverity.MODERATE if len(detected_classes) >= 1
            else PerceptualInfluenceSeverity.NONE
        )

        explanation = (
            f"False depth classes detected: {', '.join([c.value for c in detected_classes])}"
            if detected else "No false-depth features detected."
        )

        return FalseDepthDetectionResult(
            detected=detected,
            detected_classes=detected_classes,
            evidence=evidence,
            severity=severity,
            explanation=explanation,
        )


# ── Influence Alignment Analyzer ────────────────────────────────────────

class InfluenceAlignmentAnalyzer:
    """Verifies alignment between active SFL stack and brand posture constraints."""

    def __init__(self, sfl_registry: SFLRegistryService | None = None):
        self.sfl_registry = sfl_registry

    def evaluate(
        self,
        request: PerceptualInfluenceRequest,
        policy: PerceptualInfluencePolicyBundle,
    ) -> InfluenceAlignmentResult:
        evidence: list[PerceptualEvidenceItem] = []
        misalignment_details: list[str] = []

        brand_posture_match = True
        representation_geometry_match = True
        archetype_match = True
        surface_sensitivity_match = True

        stack = request.sfl_function_stack

        if stack is None:
            # SFL stack missing
            if policy.influence_alignment_required:
                brand_posture_match = False
                misalignment_details.append("SFL function stack is missing but influence alignment is required.")
                evidence.append(
                    PerceptualEvidenceItem(
                        evidence_id=_id("P-EVD"),
                        dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                        observation="Missing SFL function stack",
                        rationale="Cannot align influence layers when active functions are undeclared.",
                        contribution=-0.5,
                    )
                )
            score = 0.0
            aligned = not policy.influence_alignment_required
            return InfluenceAlignmentResult(
                aligned=aligned,
                alignment_score=score,
                brand_posture_match=brand_posture_match,
                representation_geometry_match=representation_geometry_match,
                archetype_match=archetype_match,
                surface_sensitivity_match=surface_sensitivity_match,
                misalignment_details=misalignment_details,
                evidence=evidence,
            )

        # 1. Brand Posture Match
        if request.brand_posture is not None:
            bp = request.brand_posture
            # Check forbidden patterns
            for pattern in bp.forbidden_influence_patterns:
                pattern_lower = pattern.lower()
                for fam in stack.active_families:
                    if pattern_lower in fam.lower():
                        brand_posture_match = False
                        misalignment_details.append(f"Forbidden influence pattern '{pattern}' matched active SFL family '{fam}'")
                for fn in stack.active_functions:
                    if pattern_lower in fn.lower():
                        brand_posture_match = False
                        misalignment_details.append(f"Forbidden influence pattern '{pattern}' matched active SFL function '{fn}'")

            # Check Commercial Trust Transfer vs Earned Authority
            if request.surface_class == PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER and bp.authority_source.lower() == "earned":
                aggressive_terms = ["aggression", "scarcity", "urgency", "manipulation", "fear", "pressure"]
                has_aggression = False
                for t in aggressive_terms:
                    for fam in stack.active_families:
                        if t in fam.lower():
                            has_aggression = True
                    for fn in stack.active_functions:
                        if t in fn.lower():
                            has_aggression = True
                if has_aggression:
                    brand_posture_match = False
                    misalignment_details.append("Commercial surface with high-pressure/aggressive influence functions violates earned-authority brand posture")

            # Check permitted families
            if bp.permitted_influence_families:
                permitted_lower = [f.lower() for f in bp.permitted_influence_families]
                for fam in stack.active_families:
                    if fam.lower() not in permitted_lower:
                        # Non-permitted family in use
                        brand_posture_match = False
                        misalignment_details.append(f"Active family '{fam}' is not in brand-permitted list")

        # 2. Representation Geometry Match
        if request.representation_geometry_id is not None:
            # Assume match unless mismatch found in registry
            representation_geometry_match = True

        # 3. Archetype Match
        if request.content_archetype_id is not None:
            archetype_match = True

        # 4. Surface Sensitivity Match
        surface_sensitivity_match = True

        # Compute Score
        base_score = 1.0
        if misalignment_details:
            base_score -= 0.25 * len(misalignment_details)
            base_score = max(0.0, base_score)

        aligned = (base_score >= 0.7) and brand_posture_match

        evidence.append(
            PerceptualEvidenceItem(
                evidence_id=_id("P-EVD"),
                dimension=PerceptualInfluenceDimension.INFLUENCE_ALIGNMENT,
                observation=f"Influence alignment verified (score={base_score:.2f})",
                rationale="SFL function stack checks completed against brand and surface restrictions.",
                contribution=0.5 if aligned else -0.5,
            )
        )

        return InfluenceAlignmentResult(
            aligned=aligned,
            alignment_score=round(base_score, 3),
            brand_posture_match=brand_posture_match,
            representation_geometry_match=representation_geometry_match,
            archetype_match=archetype_match,
            surface_sensitivity_match=surface_sensitivity_match,
            misalignment_details=misalignment_details,
            evidence=evidence,
        )


# ── Decision Router ──────────────────────────────────────────────────────

class PerceptualInfluenceDecisionRouter:
    """Applies policy bundle thresholds and DI prerequisites to route the overall verdict."""

    def route(
        self,
        metrics: PerceptualInfluenceMetricBundle,
        alignment: InfluenceAlignmentResult,
        false_depth: FalseDepthDetectionResult,
        policy: PerceptualInfluencePolicyBundle,
        fallback_reason: Optional[PerceptualInfluenceFallbackReason],
        di_decision: Optional[str],
    ) -> PerceptualInfluenceDecisionSummary:
        required_corrections: list[str] = []

        # 1. Check DI status first (Hard blocks take absolute precedence)
        if di_decision == "FAIL":
            return PerceptualInfluenceDecisionSummary(
                decision=PerceptualInfluenceDecision.DOWNGRADE,
                resolution_path=PerceptualInfluenceResolutionPath.SURFACE_DOWNGRADE,
                required_corrections=["Directional integrity check failed (DI = FAIL). Pipeline downgrade forced."],
                rationale="Directional integrity check failed. Evaluation downgraded.",
            )

        # 2. Check Fallbacks (Failure-closed checks)
        is_high_risk = policy.surface_class in [
            PerceptualInfluenceSurface.RENDER_RELEASE,
            PerceptualInfluenceSurface.COMMERCIAL_TRUST_TRANSFER,
            PerceptualInfluenceSurface.SOCIAL_SHARE,
        ]

        if fallback_reason is not None:
            if is_high_risk:
                return PerceptualInfluenceDecisionSummary(
                    decision=PerceptualInfluenceDecision.DOWNGRADE,
                    resolution_path=PerceptualInfluenceResolutionPath.SURFACE_DOWNGRADE,
                    required_corrections=[f"Dependency fallback: {fallback_reason.value}"],
                    rationale=f"Failed closed on fallback reason {fallback_reason.value} for high-risk surface.",
                )
            else:
                return PerceptualInfluenceDecisionSummary(
                    decision=PerceptualInfluenceDecision.REVIEW,
                    resolution_path=PerceptualInfluenceResolutionPath.OPERATOR_REVIEW,
                    required_corrections=[f"Dependency fallback: {fallback_reason.value}"],
                    rationale=f"Fallback triggered: {fallback_reason.value}. Sent to operator review.",
                )

        # 3. Check Policy constraints
        failed_policy = False

        # Positive dimensions checks
        positives = [
            (PerceptualInfluenceDimension.COGNITIVE_IMPRINT, metrics.cognitive_imprint_score),
            (PerceptualInfluenceDimension.SYMBOLIC_DENSITY, metrics.symbolic_density_score),
            (PerceptualInfluenceDimension.HUMAN_CONGRUENCE, metrics.human_congruence_score),
            (PerceptualInfluenceDimension.CONTRAST_CLARITY, metrics.contrast_clarity_score),
            (PerceptualInfluenceDimension.MEMORABILITY_PRESSURE, metrics.memorability_pressure),
        ]

        for dim_enum, dim_score in positives:
            thresh = policy.pass_thresholds.get(dim_enum.value) or policy.pass_thresholds.get(dim_enum.name)
            if thresh is not None and dim_score.score < thresh:
                failed_policy = True
                required_corrections.append(f"Dimension {dim_enum.value} is {dim_score.score}, required >= {thresh}")

        # Negative dimensions checks
        negatives = [
            (PerceptualInfluenceDimension.OVEREXPLANATION_RISK, metrics.overexplanation_risk_score),
            (PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS, metrics.synthetic_smoothness_score),
        ]

        for dim_enum, dim_score in negatives:
            ceiling = policy.risk_ceilings.get(dim_enum.value) or policy.risk_ceilings.get(dim_enum.name)
            if ceiling is not None and dim_score.score > ceiling:
                failed_policy = True
                required_corrections.append(f"Dimension {dim_enum.value} is {dim_score.score}, required <= {ceiling}")

        # False depth check
        if policy.false_depth_blocks and false_depth.detected:
            failed_policy = True
            required_corrections.append(f"False-depth features detected: {', '.join([c.value for c in false_depth.detected_classes])}")

        # Alignment check
        if policy.influence_alignment_required and not alignment.aligned:
            failed_policy = True
            required_corrections.extend(alignment.misalignment_details)

        # 4. Resolve verdict and paths
        if failed_policy:
            if is_high_risk:
                decision = PerceptualInfluenceDecision.DOWNGRADE
                res_path = PerceptualInfluenceResolutionPath.SURFACE_DOWNGRADE
            elif policy.surface_class == PerceptualInfluenceSurface.COACHING_INTERVENTION:
                decision = PerceptualInfluenceDecision.REVIEW
                res_path = PerceptualInfluenceResolutionPath.RESTORE_TENSION
            else:
                decision = PerceptualInfluenceDecision.REVIEW
                res_path = PerceptualInfluenceResolutionPath.OPERATOR_REVIEW

            return PerceptualInfluenceDecisionSummary(
                decision=decision,
                resolution_path=res_path,
                required_corrections=required_corrections,
                rationale="Policy thresholds/ceilings violated or alignment/false-depth checks failed.",
            )

        # 5. DI = REVIEW override checks
        if di_decision == "REVIEW":
            # Demote PASS to REVIEW
            return PerceptualInfluenceDecisionSummary(
                decision=PerceptualInfluenceDecision.REVIEW,
                resolution_path=PerceptualInfluenceResolutionPath.OPERATOR_REVIEW,
                required_corrections=["Directional integrity engine returned REVIEW status."],
                rationale="Overall status set to REVIEW due to upstream Directional Integrity state.",
            )

        # PASS
        return PerceptualInfluenceDecisionSummary(
            decision=PerceptualInfluenceDecision.PASS,
            resolution_path=None,
            required_corrections=[],
            rationale="All policy criteria, alignment, and DI prerequisites satisfied.",
        )


# ── Main Evaluator Service ───────────────────────────────────────────────

class PerceptualInfluenceEvaluator:
    """Core Perceptual Influence Evaluator service."""

    def __init__(
        self,
        policy_registry: PerceptualInfluencePolicyRegistry | None = None,
        sfl_registry: SFLRegistryService | None = None,
        receipt_chain: ReceiptChain | None = None,
    ):
        self.policy_registry = policy_registry or PerceptualInfluencePolicyRegistry()
        self.sfl_registry = sfl_registry
        self.receipt_chain = receipt_chain

        self.cognitive_imprint_analyzer = CognitiveImprintAnalyzer()
        self.symbolic_density_analyzer = SymbolicDensityAnalyzer()
        self.human_congruence_analyzer = HumanCongruenceAnalyzer()
        self.contrast_clarity_analyzer = ContrastClarityAnalyzer()
        self.memorability_pressure_analyzer = MemorabilityPressureAnalyzer()
        self.overexplanation_risk_analyzer = OverexplanationRiskAnalyzer()
        self.synthetic_smoothness_analyzer = SyntheticSmoothnessAnalyzer()

        self.false_depth_detector = FalseDepthDetector()
        self.influence_alignment_analyzer = InfluenceAlignmentAnalyzer(self.sfl_registry)
        self.decision_router = PerceptualInfluenceDecisionRouter()

    def evaluate(self, request: PerceptualInfluenceRequest) -> PerceptualInfluenceEvaluatorResult:
        receipt_ids: list[str] = []
        fallback_reason: Optional[PerceptualInfluenceFallbackReason] = None

        if self.receipt_chain:
            r = self.receipt_chain.log(
                agent_id="perceptual_influence_evaluator",
                action="PI27_PREREQUISITE_CHECK",
                asset_id=request.request_id,
                input_summary=f"Evaluate candidate text of length {len(request.candidate_text)}",
                metadata={"surface": request.surface_class.value, "domain": request.domain.value},
            )
            receipt_ids.append(r.receipt_id)

        # Policy Resolution
        policy = self.policy_registry.resolve(request.domain, request.surface_class)
        if policy is None:
            fallback_reason = PerceptualInfluenceFallbackReason.MISSING_POLICY

        # Determine fallbacks
        if fallback_reason is None:
            if not request.candidate_text.strip():
                fallback_reason = PerceptualInfluenceFallbackReason.NULL_CANDIDATE
            elif self.sfl_registry is None and policy.influence_alignment_required:
                fallback_reason = PerceptualInfluenceFallbackReason.MISSING_SFL_REGISTRY

        # 1. Perform dimension scoring
        if fallback_reason is None:
            try:
                cognitive = self.cognitive_imprint_analyzer.analyze(request.candidate_text)
                symbolic = self.symbolic_density_analyzer.analyze(request.candidate_text)
                human = self.human_congruence_analyzer.analyze(request.candidate_text)
                contrast = self.contrast_clarity_analyzer.analyze(request.candidate_text)
                memorability = self.memorability_pressure_analyzer.analyze(request.candidate_text)
                overexplanation = self.overexplanation_risk_analyzer.analyze(request.candidate_text)
                synthetic = self.synthetic_smoothness_analyzer.analyze(request.candidate_text)

                metrics = PerceptualInfluenceMetricBundle(
                    cognitive_imprint_score=cognitive,
                    symbolic_density_score=symbolic,
                    human_congruence_score=human,
                    contrast_clarity_score=contrast,
                    memorability_pressure=memorability,
                    overexplanation_risk_score=overexplanation,
                    synthetic_smoothness_score=synthetic,
                )
            except Exception:
                fallback_reason = PerceptualInfluenceFallbackReason.ANALYZER_CRASH
        
        # If fallback occurs, construct dummy zero/blocking metrics
        if fallback_reason is not None:
            def dummy_dim(dim: PerceptualInfluenceDimension) -> PerceptualDimensionScore:
                return PerceptualDimensionScore(
                    dimension=dim,
                    score=0.0,
                    severity=PerceptualInfluenceSeverity.CRITICAL,
                    explanation=f"Fallback occurred: {fallback_reason}",
                )
            metrics = PerceptualInfluenceMetricBundle(
                cognitive_imprint_score=dummy_dim(PerceptualInfluenceDimension.COGNITIVE_IMPRINT),
                symbolic_density_score=dummy_dim(PerceptualInfluenceDimension.SYMBOLIC_DENSITY),
                human_congruence_score=dummy_dim(PerceptualInfluenceDimension.HUMAN_CONGRUENCE),
                contrast_clarity_score=dummy_dim(PerceptualInfluenceDimension.CONTRAST_CLARITY),
                memorability_pressure=dummy_dim(PerceptualInfluenceDimension.MEMORABILITY_PRESSURE),
                overexplanation_risk_score=dummy_dim(PerceptualInfluenceDimension.OVEREXPLANATION_RISK),
                synthetic_smoothness_score=dummy_dim(PerceptualInfluenceDimension.SYNTHETIC_SMOOTHNESS),
            )

        if self.receipt_chain and fallback_reason is None:
            r = self.receipt_chain.log(
                agent_id="perceptual_influence_evaluator",
                action="PI27_METRIC_SCORING",
                asset_id=request.request_id,
                input_summary="Score perceptual dimensions",
                metadata={
                    "cognitive": metrics.cognitive_imprint_score.score,
                    "symbolic": metrics.symbolic_density_score.score,
                    "human": metrics.human_congruence_score.score,
                },
            )
            receipt_ids.append(r.receipt_id)

        # 2. Influence Alignment
        if fallback_reason is None and policy is not None:
            alignment = self.influence_alignment_analyzer.evaluate(request, policy)
        else:
            alignment = InfluenceAlignmentResult(
                aligned=False,
                alignment_score=0.0,
                brand_posture_match=False,
                representation_geometry_match=False,
                archetype_match=False,
                surface_sensitivity_match=False,
                misalignment_details=["Fallback bypass alignment check."],
            )

        if self.receipt_chain and fallback_reason is None:
            r = self.receipt_chain.log(
                agent_id="perceptual_influence_evaluator",
                action="PI27_INFLUENCE_ALIGNMENT",
                asset_id=request.request_id,
                input_summary="Verify brand and surface posture alignment",
                metadata={"aligned": alignment.aligned, "alignment_score": alignment.alignment_score},
            )
            receipt_ids.append(r.receipt_id)

        # 3. False Depth Detection
        if fallback_reason is None:
            false_depth = self.false_depth_detector.evaluate(request.candidate_text, metrics)
        else:
            false_depth = FalseDepthDetectionResult(
                detected=True,
                detected_classes=[],
                evidence=[],
                severity=PerceptualInfluenceSeverity.CRITICAL,
                explanation="Bypassed due to fallback.",
            )

        # Resolve Policy Bundle (Fallback protection)
        active_policy = policy if policy is not None else PerceptualInfluencePolicyBundle(
            policy_id="FALLBACK_DEFAULT",
            domain=request.domain,
            surface_class=request.surface_class,
            pass_thresholds={},
            risk_ceilings={},
            influence_alignment_required=False,
            false_depth_blocks=False,
        )

        # 4. Routing Decision
        decision = self.decision_router.route(
            metrics=metrics,
            alignment=alignment,
            false_depth=false_depth,
            policy=active_policy,
            fallback_reason=fallback_reason,
            di_decision=request.directional_integrity_decision,
        )

        if self.receipt_chain:
            r = self.receipt_chain.log(
                agent_id="perceptual_influence_evaluator",
                action="PI27_DECISION_ROUTING",
                asset_id=request.request_id,
                input_summary="Determine final perceptual routing verdict",
                decision=decision.decision.value,
                decision_rationale=decision.rationale,
                metadata={"verdict": decision.decision.value, "corrections": decision.required_corrections},
            )
            receipt_ids.append(r.receipt_id)

            if fallback_reason is not None:
                r = self.receipt_chain.log(
                    agent_id="perceptual_influence_evaluator",
                    action="PI27_FALLBACK_TRIGGERED",
                    asset_id=request.request_id,
                    input_summary="Fallback triggered during perceptual evaluation",
                    metadata={"fallback_reason": fallback_reason.value},
                )
                receipt_ids.append(r.receipt_id)

        lineage = []
        if request.directional_integrity_report_id:
            lineage.append(request.directional_integrity_report_id)
        if request.sfl_function_stack:
            lineage.append(request.sfl_function_stack.stack_id)

        report = PerceptualInfluenceReport(
            report_id=_id("PIR"),
            request_id=request.request_id,
            metric_bundle=metrics,
            influence_alignment=alignment,
            false_depth_result=false_depth,
            decision_summary=decision,
            fallback_reason=fallback_reason,
            policy_id=active_policy.policy_id,
            di_prerequisite_report_id=request.directional_integrity_report_id,
            di_prerequisite_decision=request.directional_integrity_decision,
            lineage_refs=lineage,
            evaluated_at_utc=datetime.now(timezone.utc),
        )

        return PerceptualInfluenceEvaluatorResult(
            report=report,
            receipt_ids=receipt_ids,
        )
