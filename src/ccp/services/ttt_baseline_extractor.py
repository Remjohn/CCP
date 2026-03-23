"""
CCP FR8 TTT Enforcement Rule — TTT Baseline Extractor (Unit 4)
Extracts Temperature, Texture, Tone from session voice note → DEP-ENG-005.

Spec reference: FR8_TTT_Enforcement_Rule_Tech_Spec.md §Layer 3: Runtime Resolution
                §DEP-ENG-005 Authentication Certificate
                §Receipt Write: TTT-BASELINE-RESOLUTION

LIWC-22 authenticity gate: score ≥ 7/10 → AUTHENTICATED (AC7)
If score < 7/10 → OARS re-elicitation triggered (not in scope of this extractor — 
caller must handle the re-elicitation loop).

Writes to: config/ttt_baseline.json (DEP-ENG-005)
Receipt: TTT-BASELINE-RESOLUTION
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.ccp.models.ttt_models import (
    TextureQuality,
    ToneRegister,
    TTTBaselineData,
)

# ─── LIWC-22 Authenticity Gate ────────────────────────────────────────────────

LIWC_AUTHENTICITY_THRESHOLD = 7.0  # AC7: score ≥ 7/10 → AUTHENTICATED


class LIWCAuthenticationError(Exception):
    """Raised when LIWC-22 authenticity score is below the required threshold (AC7).

    The coach must re-record a more authentic voice note. Caller should trigger
    the OARS re-elicitation question flow.
    """

    def __init__(self, score: float, threshold: float = LIWC_AUTHENTICITY_THRESHOLD):
        self.score = score
        self.threshold = threshold
        super().__init__(
            f"LIWC-22 authenticity score {score:.1f} is below the required threshold "
            f"{threshold:.1f}/10. Coach must re-record a more authentic voice note. "
            f"Trigger OARS re-elicitation."
        )


class TTTExtractionError(Exception):
    """Raised when TTT components cannot be extracted from LIWC-22 analysis."""
    pass


class TTTBaselineExtractor:
    """Extracts TTT components from a processed LIWC-22 voice note analysis.

    Spec §Layer 3 Runtime Resolution flow:
    1. Coach voice note → LIWC-22 analysis (via FR2)
    2. Authenticity gate: score ≥ 7/10 → AUTHENTICATED (AC7)
    3. TTT extraction: Temperature (vocal markers), Texture (linguistic), Tone (semantic)
    4. Write → config/ttt_baseline.json (DEP-ENG-005)
    5. Write RECEIPT: TTT-BASELINE-RESOLUTION

    The extractor is deterministic given the LIWC-22 analysis dict.
    Caller (FR2 / Scheduled Monitor Agent) is responsible for:
    - Audio-to-LIWC-22 conversion
    - OARS re-elicitation if authentication fails
    """

    def __init__(self, coach_dir: Path):
        """Initialize the extractor.

        Args:
            coach_dir: Root directory of the coach instance.
        """
        self.coach_dir = coach_dir

    def extract(
        self,
        liwc_analysis: dict[str, Any],
        session_id: str,
        coach_id: str,
        force_authenticate: bool = False,
    ) -> TTTBaselineData:
        """Extract TTT from a LIWC-22 analysis dict.

        Args:
            liwc_analysis: LIWC-22 analysis output from FR2 voice note processing.
            session_id: The production session ID.
            coach_id: Coach person ID.
            force_authenticate: If True, bypass the LIWC authenticity gate (testing only).

        Returns:
            TTTBaselineData representing DEP-ENG-005.

        Raises:
            LIWCAuthenticationError: If LIWC-22 score < 7.0/10 (AC7) and not force_authenticate.
            TTTExtractionError: If TTT components cannot be derived from the analysis.
        """
        authenticity_score = float(liwc_analysis.get("authenticity_score", 0.0))

        # Authenticity gate (AC7)
        if not force_authenticate and authenticity_score < LIWC_AUTHENTICITY_THRESHOLD:
            raise LIWCAuthenticationError(authenticity_score)

        # Extract TTT components
        temperature = self._extract_temperature(liwc_analysis)
        texture = self._extract_texture(liwc_analysis)
        tone = self._extract_tone(liwc_analysis)

        # Voice note hash for audit trail
        voice_note_content = json.dumps(liwc_analysis, sort_keys=True, ensure_ascii=False)
        voice_note_hash = hashlib.sha256(voice_note_content.encode("utf-8")).hexdigest()

        baseline = TTTBaselineData(
            temperature=temperature,
            texture=texture,
            tone=tone,
            liwc_authenticity_score=authenticity_score,
            session_id=session_id,
            coach_id=coach_id,
            extraction_timestamp=datetime.now(timezone.utc).isoformat(),
            voice_note_hash=voice_note_hash,
            liwc_authenticated=(authenticity_score >= LIWC_AUTHENTICITY_THRESHOLD),
            raw_temperature_reading=self._raw_temperature(liwc_analysis),
        )

        return baseline

    def write(self, baseline: TTTBaselineData) -> Path:
        """Write TTT baseline to config/ttt_baseline.json (DEP-ENG-005).

        Spec §Key Files: ttt_baseline.json is the Authentication Certificate —
        primary runtime TTT resolution source.

        AC10 compliance: Writes ONLY to ttt_baseline.json. Does not modify
        coach_soul.json, voice_dna.json, or any other DEP object.

        Args:
            baseline: The extracted TTTBaselineData to write.

        Returns:
            Path to the written file.
        """
        output_path = self.coach_dir / "config" / "ttt_baseline.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(baseline.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return output_path

    def extract_and_write(
        self,
        liwc_analysis: dict[str, Any],
        session_id: str,
        coach_id: str,
        force_authenticate: bool = False,
    ) -> tuple[TTTBaselineData, Path]:
        """Extract TTT and immediately write to DEP-ENG-005.

        Args:
            liwc_analysis: LIWC-22 analysis dict from FR2.
            session_id: Production session ID.
            coach_id: Coach person ID.
            force_authenticate: Bypass LIWC gate (testing only).

        Returns:
            Tuple of (TTTBaselineData, Path to ttt_baseline.json).
        """
        baseline = self.extract(liwc_analysis, session_id, coach_id, force_authenticate)
        path = self.write(baseline)
        return baseline, path

    def load(self) -> Optional[TTTBaselineData]:
        """Load the current TTT baseline from DEP-ENG-005.

        Returns:
            TTTBaselineData if ttt_baseline.json exists, None otherwise.
        """
        baseline_path = self.coach_dir / "config" / "ttt_baseline.json"
        if not baseline_path.exists():
            return None
        try:
            data = json.loads(baseline_path.read_text(encoding="utf-8"))
            return TTTBaselineData.model_validate(data)
        except (json.JSONDecodeError, ValueError):
            return None

    # ─── Private Extraction Logic ──────────────────────────────────────────────

    def _extract_temperature(self, liwc_analysis: dict[str, Any]) -> int:
        """Extract emotional intensity (Temperature) from LIWC-22 analysis.

        Spec §Layer 3: "TEMPERATURE: Emotional intensity measured from vocal markers
        (speed, pitch variance, volume dynamics, pause patterns)"

        Maps LIWC-22 markers to TTT-01 → TTT-10 scale:
        - Positive emotion words (posemo): high posemo = higher temperature
        - Negative emotion words (negemo): high negemo = higher intensity (anger especially)
        - Affect words (affect): combined emotional activation
        - Clout score: confidence/dominance → temperature signal
        - Authenticity score: confirmed authentic = reinforces temperature reading

        Returns int in [1, 10].
        """
        # Primary: affect score (overall emotional activation)
        affect = float(liwc_analysis.get("affect", 0.0))
        posemo = float(liwc_analysis.get("posemo", 0.0))
        negemo = float(liwc_analysis.get("negemo", 0.0))
        clout = float(liwc_analysis.get("clout", 50.0))  # LIWC default is ~50

        # Combine affect and clout into temperature signal
        # affect range 0-30 typical, clout range 0-100
        affect_contribution = min(affect / 15.0, 1.0)  # Normalize to 0-1
        clout_contribution = clout / 100.0

        # Emotional intensity = weighted combination
        raw_temperature = (affect_contribution * 0.6) + (clout_contribution * 0.4)

        # Scale to [1, 10]
        temperature = max(1, min(10, round(raw_temperature * 9) + 1))
        return temperature

    def _raw_temperature(self, liwc_analysis: dict[str, Any]) -> float:
        """Extract the raw (pre-rounded) temperature float for diagnostic purposes."""
        affect = float(liwc_analysis.get("affect", 0.0))
        clout = float(liwc_analysis.get("clout", 50.0))
        affect_contribution = min(affect / 15.0, 1.0)
        clout_contribution = clout / 100.0
        return (affect_contribution * 0.6) + (clout_contribution * 0.4)

    def _extract_texture(self, liwc_analysis: dict[str, Any]) -> TextureQuality:
        """Extract stylistic surface quality (Texture) from LIWC-22 analysis.

        Spec §Layer 3: "TEXTURE: Stylistic surface quality from linguistic analysis
        (sentence complexity, metaphor density, register formality)"

        Maps LIWC-22 markers to TextureQuality scale:
        - Analytic score (high → formal/polished, low → conversational/raw)
        - Authentic score (high → raw/genuine)
        - Nonfluencies and informal markers → texture roughness
        """
        analytic = float(liwc_analysis.get("analytic", 50.0))
        authentic = float(liwc_analysis.get("authentic", 50.0))
        informal = float(liwc_analysis.get("informal", 0.0))

        # Combine signals:
        # High analytic + low informal = literary/polished
        # High authentic + high informal = raw/colloquial
        polish_score = (analytic / 100.0) * 0.7 - (informal / 20.0) * 0.3

        if polish_score >= 0.6:
            return TextureQuality.LITERARY
        elif polish_score >= 0.35:
            return TextureQuality.POLISHED
        elif polish_score >= 0.10:
            return TextureQuality.CONVERSATIONAL
        elif polish_score >= -0.15:
            return TextureQuality.COLLOQUIAL
        else:
            return TextureQuality.RAW

    def _extract_tone(self, liwc_analysis: dict[str, Any]) -> ToneRegister:
        """Extract vocal register (Tone) from LIWC-22 analysis.

        Spec §Layer 3: "TONE: Vocal register classification from semantic analysis
        (confrontational, reflective, nurturing, instructional)"

        Maps LIWC-22 semantic categories to ToneRegister:
        - High anger/negemo + high clout → CONFRONTATIONAL
        - High posemo + social words → NURTURING
        - High insight/cogmech → REFLECTIVE
        - High drive/achieve + low negemo → INSTRUCTIONAL
        - Others → best-fit mapping
        """
        anger = float(liwc_analysis.get("anger", 0.0))
        posemo = float(liwc_analysis.get("posemo", 0.0))
        negemo = float(liwc_analysis.get("negemo", 0.0))
        social = float(liwc_analysis.get("social", 0.0))
        insight = float(liwc_analysis.get("insight", 0.0))
        cogmech = float(liwc_analysis.get("cogmech", 0.0))
        clout = float(liwc_analysis.get("clout", 50.0))
        achieve = float(liwc_analysis.get("achieve", 0.0))
        power = float(liwc_analysis.get("power", 0.0))

        # Score each register
        confrontational_score = (anger * 2) + (negemo * 0.5) + (clout / 100 * 3)
        nurturing_score = (posemo * 1.5) + (social * 1.2) - (anger * 1.0)
        reflective_score = (insight * 2) + (cogmech * 1.5) - (clout / 100 * 2)
        instructional_score = (achieve * 1.5) + (power * 1.0) + (clout / 100 * 1.5)

        scores = {
            ToneRegister.CONFRONTATIONAL: confrontational_score,
            ToneRegister.NURTURING: nurturing_score,
            ToneRegister.REFLECTIVE: reflective_score,
            ToneRegister.INSTRUCTIONAL: instructional_score,
        }

        # Return the highest-scoring register
        return max(scores, key=lambda k: scores[k])
