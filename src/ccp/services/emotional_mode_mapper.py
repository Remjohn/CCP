"""
CCP FR6 — Emotional Mode Mapper (Phase B3) (Unit 4)
T/V/R emotional mode classification with intensity and activation conditions.

Spec reference: FR6 Tech Spec §Phase B3
  T = Tension (confrontation, common enemies, wounds, injustices)
  V = Vulnerability (private pain, core anxieties, unspoken fears, taboos)
  R = Recognition (belonging, rituals, insider language, shared memories)

Gate: ≥3 triggers per mode. If any mode <3 → MODE-INCOMPLETE.

Content routing implications:
  T → high-temperature archetypes (TTT-07+): myth_indignation, reaction_outrage
  V → low-temperature archetypes (TTT-02/03): story_transformation, story_recognition
  R → recognition archetypes: tweet_recognition, listicle_relatable
"""

from src.ccp.models.tribe_profile_models import (
    EmotionalMode,
    EmotionalTriggerEntry,
    ModeDistribution,
    TriggerIntensity,
)


# Keyword sets for mode classification heuristics
_TENSION_KEYWORDS = frozenset([
    "enemy", "injustice", "unfair", "fight", "wrong", "rigged",
    "corrupt", "oppression", "outrage", "anger", "betrayal",
    "exploitation", "neglect", "discrimination", "manipulation",
    "fraud", "stolen", "lie", "cheat", "abuse", "systemic",
])

_VULNERABILITY_KEYWORDS = frozenset([
    "afraid", "scared", "fear", "anxiety", "shame", "lonely",
    "isolated", "broken", "hurt", "pain", "crying", "depression",
    "overwhelmed", "helpless", "hopeless", "insecure", "doubt",
    "worthless", "invisible", "abandoned", "grief", "trauma",
])

_RECOGNITION_KEYWORDS = frozenset([
    "remember", "ritual", "tradition", "home", "belong",
    "nostalgia", "community", "family", "together", "our",
    "we", "insider", "recognize", "identity", "culture",
    "heritage", "roots", "bond", "shared", "celebrate",
])


class EmotionalModeMapper:
    """FR6 Phase B3: T/V/R Emotional Mode Mapping.

    For each trigger/celebration/grief pattern/solidarity signal,
    classifies the emotional mode and intensity.

    AC5: ≥3 triggers per mode (T/V/R). A profile with 10 Tension triggers,
    4 Vulnerability triggers, 0 Recognition triggers → MODE-INCOMPLETE.
    """

    def classify_mode(
        self,
        text: str,
        activation_keywords: list[str] | None = None,
    ) -> EmotionalMode:
        """Classify a text entry to T/V/R mode.

        Uses keyword frequency across the three mode vocabularies.
        Activation keywords provide additional signal if present.
        """
        text_lower = text.lower()
        words = set(text_lower.split())
        all_keywords = set(activation_keywords or [])
        combined = words | {k.lower() for k in all_keywords}

        t_score = len(combined & _TENSION_KEYWORDS)
        v_score = len(combined & _VULNERABILITY_KEYWORDS)
        r_score = len(combined & _RECOGNITION_KEYWORDS)

        if t_score >= v_score and t_score >= r_score:
            return EmotionalMode.TENSION
        elif v_score >= r_score:
            return EmotionalMode.VULNERABILITY
        else:
            return EmotionalMode.RECOGNITION

    def classify_intensity(
        self,
        text: str,
        engagement_signals: dict[str, float] | None = None,
    ) -> TriggerIntensity:
        """Classify trigger intensity: dormant / active / nuclear.

        Nuclear: multiple intensity markers + high engagement.
        Active: present with clear emotional charge.
        Dormant: mentioned but without activation energy.
        """
        text_lower = text.lower()
        nuclear_markers = [
            "always", "every time", "never forget", "can't stop",
            "obsess", "rage", "fury", "unbearable", "intolerable",
            "consumed", "haunts me", "kills me", "destroys",
        ]
        active_markers = [
            "feel", "trigger", "react", "respond", "notice",
            "bother", "annoy", "frustrat", "upset", "affect",
        ]

        nuclear_count = sum(1 for m in nuclear_markers if m in text_lower)
        active_count = sum(1 for m in active_markers if m in text_lower)

        if nuclear_count >= 2:
            return TriggerIntensity.NUCLEAR
        elif nuclear_count >= 1 or active_count >= 2:
            return TriggerIntensity.ACTIVE
        else:
            return TriggerIntensity.DORMANT

    def map_triggers(
        self,
        triggers: list[EmotionalTriggerEntry],
    ) -> list[EmotionalTriggerEntry]:
        """Classify mode and intensity for a list of emotional triggers."""
        for trigger in triggers:
            trigger.mode = self.classify_mode(
                text=trigger.text,
                activation_keywords=trigger.activation_keywords,
            )
            trigger.intensity = self.classify_intensity(text=trigger.text)
        return triggers

    def compute_mode_distribution(
        self,
        triggers: list[EmotionalTriggerEntry],
    ) -> ModeDistribution:
        """Compute T/V/R distribution. AC5: ≥3 per mode."""
        t_count = sum(1 for t in triggers if t.mode == EmotionalMode.TENSION)
        v_count = sum(1 for t in triggers if t.mode == EmotionalMode.VULNERABILITY)
        r_count = sum(1 for t in triggers if t.mode == EmotionalMode.RECOGNITION)

        return ModeDistribution(
            tension_count=t_count,
            vulnerability_count=v_count,
            recognition_count=r_count,
        )

    def validate_mode_gate(
        self,
        distribution: ModeDistribution,
    ) -> bool:
        """Spec §Phase B3 Gate: ≥3 triggers per mode.
        AC5: Fails if any mode <3."""
        return distribution.passes_mode_gate()

    def get_mode_incomplete_modes(
        self,
        distribution: ModeDistribution,
    ) -> list[str]:
        """Return list of modes that are incomplete (<3 triggers)."""
        incomplete: list[str] = []
        if distribution.tension_count < 3:
            incomplete.append("Tension")
        if distribution.vulnerability_count < 3:
            incomplete.append("Vulnerability")
        if distribution.recognition_count < 3:
            incomplete.append("Recognition")
        return incomplete
