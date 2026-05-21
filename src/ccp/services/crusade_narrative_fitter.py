"""Crusade Narrative Fitter — FR-ERA3-04 / DEP-OFO-002.
Wraps raw biometric scores in Epic Meaning Framing (Phase5-M03).
Deterministic fallback logic when LLM output fails validation."""
from __future__ import annotations
from typing import Any
from src.ccp.models.ofo_models import (
    CRUSADE_FALLBACK_TEMPLATES, CrusadeNarrativeAudit,
)


class CrusadeNarrativeFitter:
    """Translates raw biometric scores into ego-defended narrative scripts.

    Phase5-M03 enforcement: All biometric flaws are framed as externally caused
    by algorithmic compression, not as personal failings.

    If LLM generation fails the Pydantic regex check, falls back to
    pre-approved deterministic template strings (§4 Phase 3 Step 10).
    """

    def __init__(self, *, llm_client: Any = None) -> None:
        self._llm = llm_client

    def apply_framing(self, *, detected_flaw: str, biometric_score: float,
                      raw_traits: list[dict] | None = None) -> CrusadeNarrativeAudit:
        """Generate a validated Crusade Narrative transcript.

        Args:
            detected_flaw: The primary biometric negative metric (e.g., 'Embodied Confidence').
            biometric_score: The raw score (0-10 scale).
            raw_traits: Optional list of all scored traits for context.

        Returns:
            Validated CrusadeNarrativeAudit that passes Phase5-M03 constraints.
        """
        # Attempt LLM generation if client available
        if self._llm:
            llm_transcript = self._attempt_llm_generation(
                detected_flaw=detected_flaw, biometric_score=biometric_score,
                raw_traits=raw_traits,
            )
            if llm_transcript:
                try:
                    return CrusadeNarrativeAudit(
                        transcript=llm_transcript,
                        detected_flaw=detected_flaw,
                        biometric_score=biometric_score,
                    )
                except ValueError:
                    # LLM output failed Phase5-M03 validation — fall through to deterministic
                    pass

        # Deterministic fallback (§4 Phase 3 Step 10)
        return self._deterministic_fallback(detected_flaw=detected_flaw, biometric_score=biometric_score)

    def apply_baseline_discovery(self) -> CrusadeNarrativeAudit:
        """Generate Baseline Discovery narrative when audio quality is too poor (§4 Phase 3 Step 12).

        Blames social media compression for the poor audio and requests clean Telegram voice note.
        """
        return CrusadeNarrativeAudit(
            transcript=CRUSADE_FALLBACK_TEMPLATES["baseline_discovery"],
            detected_flaw="Insufficient Audio Signal",
            biometric_score=0.0,
        )

    def _attempt_llm_generation(self, *, detected_flaw: str, biometric_score: float,
                                raw_traits: list[dict] | None) -> str | None:
        """Attempt LLM transcript generation with Crusade Narrative context."""
        prompt = self._build_prompt(detected_flaw=detected_flaw, biometric_score=biometric_score)
        try:
            response = self._llm.generate(prompt)
            if response and isinstance(response, str) and len(response) > 50:
                return response
        except Exception:
            pass
        return None

    def _build_prompt(self, *, detected_flaw: str, biometric_score: float) -> str:
        return (
            f"Generate a 150-word voiceover script for an Animated Video Audit. "
            f"The detected biometric flaw is '{detected_flaw}' with a score of {biometric_score}/10. "
            f"CRITICAL RULES: "
            f"1. Frame ALL critique against 'the algorithm' or 'platform compression' — NEVER against the coach. "
            f"2. You MUST include at least 2 of these words: algorithm, compression, flattening, legacy, defend, protect. "
            f"3. You MUST NOT use: poor, weak, bad, inadequate, 'needs improvement'. "
            f"4. Position CCP as the coach's elite ally defending their legacy against algorithmic erosion. "
            f"5. End with a call to action to record a 60-second correction."
        )

    def _deterministic_fallback(self, *, detected_flaw: str, biometric_score: float) -> CrusadeNarrativeAudit:
        """Select and return a pre-approved deterministic template."""
        flaw_key = detected_flaw.lower().replace(" ", "_")
        template = CRUSADE_FALLBACK_TEMPLATES.get(flaw_key, CRUSADE_FALLBACK_TEMPLATES["default"])
        return CrusadeNarrativeAudit(
            transcript=template,
            detected_flaw=detected_flaw,
            biometric_score=biometric_score,
        )
