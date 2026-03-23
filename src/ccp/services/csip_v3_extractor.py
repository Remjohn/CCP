"""
CCP FR4 Emotional DNA — CSIP v3.0 Extension Extractor (Unit 5)
Phase 4: Extract behavioral extension variables EXT-1 through EXT-5.

Spec reference: FR4 Tech Spec §Phase 4 REASON (CSIP v3.0 extensions)
Research basis: Coaching-Specific Interaction Parameters v3.0

EXT-1: Emotion Residency Time per register
        (SHORT <2 sentences, MEDIUM 3-5, LONG 6+)
EXT-2: Emotional Ceiling per Topic cluster
        (max TTT reached on topic clusters)
EXT-3: Emotional Floor per Topic cluster
        (baseline/min TTT on topic clusters)
EXT-4: Suppression Patterns
        (compression artifacts — sudden brevity, topic pivots,
         unanswered rhetorical questions)
EXT-5: Resolution Pattern + Emotional Bleed Signatures
        (resolves/leaves_open/converts + bleed-between-registers)

Mandate 7 enforced: every variable requires corpus citation.
"""

import re

from src.ccp.models.emotional_dna_models import (
    EmotionalBleedSignature,
    EmotionalCeilingPerTopic,
    EmotionalFloorPerTopic,
    EmotionResidencyTime,
    EvidencePassage,
    ResidencyTime,
    ResolutionPattern,
    ResolutionPatternType,
    SuppressionPattern,
    SuppressionPatterns,
    CSIPv3Extensions,
    TopicCeiling,
    TopicFloor,
)


# ──────────────────────────────────────────────────────────────
# Emotional Registers (Spec §Phase 4 EXT-1)
# ──────────────────────────────────────────────────────────────

EMOTIONAL_REGISTERS: dict[str, list[str]] = {
    "disgust": [
        r"\b(disgust|disgusting|revolting|repulsive|sickening|nauseating|gross)\b",
    ],
    "outrage": [
        r"\b(outrage|outrageous|infuriating|furious|enraged|incensed|livid)\b",
    ],
    "grief": [
        r"\b(grief|grieving|heartbroken|devastated|mourning|loss|bereft)\b",
    ],
    "tenderness": [
        r"\b(tender|tenderness|compassion|warm|moved|touched|empathy|care)\b",
    ],
    "conviction": [
        r"\b(conviction|convicted|believe deeply|know in my bones|certain|absolute)\b",
    ],
    "urgency": [
        r"\b(urgent|urgency|must act|now|immediately|critical|time is|hurry)\b",
    ],
}


# ──────────────────────────────────────────────────────────────
# Topic Cluster Detection
# ──────────────────────────────────────────────────────────────

TOPIC_CLUSTERS: dict[str, list[str]] = {
    "money_pricing": [
        r"\b(money|price|pricing|cost|fee|charge|invest|revenue|profit|income)\b",
    ],
    "identity_purpose": [
        r"\b(identity|purpose|calling|mission|who I am|why I exist|self-worth)\b",
    ],
    "industry_ethics": [
        r"\b(industry|ethics|ethical|unethical|practice|standard|certification)\b",
    ],
    "client_transformation": [
        r"\b(client|transformation|result|outcome|impact|change|growth|progress)\b",
    ],
    "personal_story": [
        r"\b(my story|my experience|I remember|back when|personally|my life)\b",
    ],
    "systems_structures": [
        r"\b(system|structure|institution|organization|framework|paradigm|model)\b",
    ],
}


# ──────────────────────────────────────────────────────────────
# Suppression Artifact Patterns (EXT-4)
# ──────────────────────────────────────────────────────────────

SUDDEN_BREVITY_PATTERNS: list[str] = [
    r"(?:^|\. )(?:\w+[\s,]*){1,5}[.!?]$",  # Very short sentence after long ones
]

TOPIC_PIVOT_MARKERS: list[str] = [
    r"\b(anyway|moving on|but let me|so back to|let's talk about)\b",
    r"\b(a different topic|something else|on another note|regardless)\b",
]

UNANSWERED_RHETORICAL_MARKERS: list[str] = [
    r"[^?]*\?\s*(?:And|But|So|Because|The thing|Look)",
    r"[^?]*\?\s+[A-Z]",  # Question followed immediately by a new sentence
]


# ──────────────────────────────────────────────────────────────
# Resolution & Bleed Patterns (EXT-5)
# ──────────────────────────────────────────────────────────────

RESOLUTION_MARKERS: list[str] = [
    r"\b(in the end|ultimately|so I|resolved|settled|accepted|moved on)\b",
    r"\b(found peace|let go|came to terms|conclusion is|bottom line)\b",
]

LEAVES_OPEN_MARKERS: list[str] = [
    r"\b(I still don't know|unresolved|I'm not sure|haven't figured)\b",
    r"\b(it's complicated|no easy answer|open question|I wonder)\b",
]

CONVERTS_MARKERS: list[str] = [
    r"\b(channeled into|turned into|became fuel|transformed into|converted)\b",
    r"\b(that anger became|my grief became|use that|redirect)\b",
]

BLEED_MARKERS: list[str] = [
    r"\b(no[,\s]+I'm|wait[,\s]+I'm actually|I mean[,\s]+I'm)\b",
    r"(—\s*no\s*,?\s*I)",
    r"\b(started as \w+ (?:but|and) (?:became|turned into))\b",
]


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def _count_matches(text: str, patterns: list[str]) -> int:
    """Count total regex matches across patterns."""
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    return count


def _find_sentences_with_patterns(
    sentences: list[str],
    patterns: list[str],
    label: str,
    session_id: str,
    max_passages: int = 10,
) -> list[EvidencePassage]:
    """Find sentences matching any pattern."""
    passages: list[EvidencePassage] = []
    for idx, sent in enumerate(sentences):
        for pattern in patterns:
            if re.search(pattern, sent, re.IGNORECASE):
                passages.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label=label,
                    source_session_id=session_id,
                ))
                break
        if len(passages) >= max_passages:
            break
    return passages


class CSIPv3Extractor:
    """Extracts EXT-1 through EXT-5 CSIP v3.0 behavioral extensions.

    Spec §Phase 4: Forensic analysis of emotional register behavior,
    topic-cluster intensity patterns, suppression artifacts, and
    resolution/bleed dynamics.
    """

    def extract(
        self,
        corpus_text: str,
        session_id: str = "",
    ) -> CSIPv3Extensions:
        """Extract all 5 CSIP v3 extension variables.

        Args:
            corpus_text: Full concatenated corpus text.
            session_id: Source session ID for evidence provenance.

        Returns:
            CSIPv3Extensions with all extractable extensions populated.
        """
        sentences = _split_into_sentences(corpus_text)

        result = CSIPv3Extensions()
        result.emotion_residency_time = self._extract_ext1(
            sentences, session_id
        )
        result.emotional_ceiling_per_topic = self._extract_ext2(
            sentences, session_id
        )
        result.emotional_floor_per_topic = self._extract_ext3(
            sentences, session_id
        )
        result.suppression_patterns = self._extract_ext4(
            sentences, session_id
        )

        resolution_result = self._extract_ext5(sentences, session_id)
        result.resolution_pattern = resolution_result[0]
        result.emotional_bleed_signatures = resolution_result[1]

        return result

    def _extract_ext1(
        self,
        sentences: list[str],
        session_id: str,
    ) -> EmotionResidencyTime:
        """Spec §Phase 4 EXT-1: Emotion Residency Time per register.

        Measurement: For each emotional register, find contiguous sentences
        where register is active. Classify:
          SHORT: <2 sentences sustained
          MEDIUM: 3-5 sentences sustained
          LONG: 6+ sentences sustained
        """
        per_register: dict[str, ResidencyTime] = {}
        all_evidence: list[EvidencePassage] = []

        for register, patterns in EMOTIONAL_REGISTERS.items():
            # Find runs of consecutive sentences matching this register
            runs = self._find_consecutive_runs(sentences, patterns)
            if not runs:
                continue

            # Take the longest run as the representative residency
            longest_run = max(runs, key=len)
            run_length = len(longest_run)

            if run_length < 2:
                residency = ResidencyTime.SHORT
            elif run_length <= 5:
                residency = ResidencyTime.MEDIUM
            else:
                residency = ResidencyTime.LONG

            per_register[register] = residency

            # Collect evidence from the longest run
            for idx, sent in enumerate(longest_run[:3]):  # max 3 evidence
                all_evidence.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label=f"residency_{register}_{residency.value}",
                    source_session_id=session_id,
                ))

        if not per_register:
            return EmotionResidencyTime()

        return EmotionResidencyTime(
            per_register=per_register,
            evidence_passages=all_evidence,
        )

    def _find_consecutive_runs(
        self,
        sentences: list[str],
        patterns: list[str],
    ) -> list[list[str]]:
        """Find runs of consecutive sentences matching any pattern."""
        runs: list[list[str]] = []
        current_run: list[str] = []

        for sent in sentences:
            has_match = False
            for pattern in patterns:
                if re.search(pattern, sent, re.IGNORECASE):
                    has_match = True
                    break
            if has_match:
                current_run.append(sent)
            else:
                if current_run:
                    runs.append(current_run)
                    current_run = []

        if current_run:
            runs.append(current_run)

        return runs

    def _extract_ext2(
        self,
        sentences: list[str],
        session_id: str,
    ) -> EmotionalCeilingPerTopic:
        """Spec §Phase 4 EXT-2: Emotional Ceiling per Topic cluster.

        For each topic, find the peak emotional intensity (highest TTT)
        and the construction signature at ceiling.
        """
        ceilings: list[TopicCeiling] = []

        for topic, patterns in TOPIC_CLUSTERS.items():
            topic_sentences = []
            for idx, sent in enumerate(sentences):
                for pattern in patterns:
                    if re.search(pattern, sent, re.IGNORECASE):
                        topic_sentences.append((idx, sent))
                        break

            if not topic_sentences:
                continue

            # Score emotional intensity per sentence
            max_intensity = 0
            max_sentence = ""
            max_idx = 0

            for idx, sent in topic_sentences:
                intensity = self._score_emotional_intensity(sent)
                if intensity > max_intensity:
                    max_intensity = intensity
                    max_sentence = sent
                    max_idx = idx

            if max_intensity > 0:
                evidence = [EvidencePassage(
                    passage_text=max_sentence.strip(),
                    passage_index=max_idx,
                    label=f"ceiling_{topic}_{max_intensity}",
                    source_session_id=session_id,
                )]
                ttt_label = self._intensity_to_ttt(max_intensity)
                ceilings.append(TopicCeiling(
                    topic=topic,
                    max_ttt=ttt_label,
                    construction_signature_at_ceiling=self._identify_construction(
                        max_sentence
                    ),
                    evidence_passages=evidence,
                ))

        return EmotionalCeilingPerTopic(topic_ceilings=ceilings)

    def _extract_ext3(
        self,
        sentences: list[str],
        session_id: str,
    ) -> EmotionalFloorPerTopic:
        """Spec §Phase 4 EXT-3: Emotional Floor per Topic cluster.

        For each topic, find the baseline/minimum emotional intensity.
        """
        floors: list[TopicFloor] = []

        for topic, patterns in TOPIC_CLUSTERS.items():
            topic_sentences = []
            for idx, sent in enumerate(sentences):
                for pattern in patterns:
                    if re.search(pattern, sent, re.IGNORECASE):
                        topic_sentences.append((idx, sent))
                        break

            if len(topic_sentences) < 2:
                continue

            # Find minimum intensity sentence
            min_intensity = 999
            min_sentence = ""
            min_idx = 0

            for idx, sent in topic_sentences:
                intensity = self._score_emotional_intensity(sent)
                if intensity < min_intensity:
                    min_intensity = intensity
                    min_sentence = sent
                    min_idx = idx

            evidence = [EvidencePassage(
                passage_text=min_sentence.strip(),
                passage_index=min_idx,
                label=f"floor_{topic}_{min_intensity}",
                source_session_id=session_id,
            )]
            ttt_label = self._intensity_to_ttt(min_intensity)
            floors.append(TopicFloor(
                topic=topic,
                min_ttt=ttt_label,
                evidence_passages=evidence,
            ))

        return EmotionalFloorPerTopic(topic_floors=floors)

    def _extract_ext4(
        self,
        sentences: list[str],
        session_id: str,
    ) -> SuppressionPatterns:
        """Spec §Phase 4 EXT-4: Suppression Patterns.

        Compression artifacts:
        1. Sudden brevity after emotional build-up
        2. Topic pivots (abrupt subject changes)
        3. Unanswered rhetorical questions
        """
        patterns_found: list[SuppressionPattern] = []

        # 1. Sudden brevity detection
        for i in range(2, len(sentences)):
            prev_len = len(sentences[i - 1].split())
            curr_len = len(sentences[i].split())

            # Previous sentence is substantial, current is very short
            if prev_len >= 15 and curr_len <= 5:
                # Check if previous had emotional content
                prev_emotional = self._score_emotional_intensity(sentences[i - 1])
                if prev_emotional >= 3:
                    # Identify which emotion was active
                    active_emotion = self._identify_active_emotion(sentences[i - 1])
                    patterns_found.append(SuppressionPattern(
                        emotion=active_emotion,
                        compression_artifact="sudden_brevity",
                        triggering_context=sentences[i - 1][:100],
                        evidence_passages=[EvidencePassage(
                            passage_text=f"{sentences[i-1]} | {sentences[i]}",
                            passage_index=i,
                            label="suppression_brevity",
                            source_session_id=session_id,
                        )],
                    ))

        # 2. Topic pivots
        pivot_evidence = _find_sentences_with_patterns(
            sentences, TOPIC_PIVOT_MARKERS, "suppression_pivot", session_id
        )
        for ev in pivot_evidence:
            # Check preceding sentence for emotional content
            if ev.passage_index > 0:
                prev_sent = sentences[ev.passage_index - 1]
                active_emotion = self._identify_active_emotion(prev_sent)
                patterns_found.append(SuppressionPattern(
                    emotion=active_emotion,
                    compression_artifact="topic_pivot",
                    triggering_context=prev_sent[:100],
                    evidence_passages=[ev],
                ))

        # 3. Unanswered rhetorical questions
        for idx, sent in enumerate(sentences):
            for pattern in UNANSWERED_RHETORICAL_MARKERS:
                if re.search(pattern, sent, re.IGNORECASE):
                    active_emotion = self._identify_active_emotion(sent)
                    patterns_found.append(SuppressionPattern(
                        emotion=active_emotion,
                        compression_artifact="unanswered_rhetorical",
                        triggering_context=sent[:100],
                        evidence_passages=[EvidencePassage(
                            passage_text=sent.strip(),
                            passage_index=idx,
                            label="suppression_rhetorical",
                            source_session_id=session_id,
                        )],
                    ))
                    break

        return SuppressionPatterns(patterns=patterns_found)

    def _extract_ext5(
        self,
        sentences: list[str],
        session_id: str,
    ) -> tuple[ResolutionPattern, list[EmotionalBleedSignature]]:
        """Spec §Phase 4 EXT-5: Resolution Pattern + Emotional Bleed.

        Resolution: resolves / leaves_open / converts
        Bleed: emotion-to-emotion transitions within passages.
        """
        # Resolution pattern classification
        resolve_count = 0
        open_count = 0
        convert_count = 0

        resolve_evidence: list[EvidencePassage] = []
        open_evidence: list[EvidencePassage] = []
        convert_evidence: list[EvidencePassage] = []

        for idx, sent in enumerate(sentences):
            resolve_hits = _count_matches(sent, RESOLUTION_MARKERS)
            open_hits = _count_matches(sent, LEAVES_OPEN_MARKERS)
            convert_hits = _count_matches(sent, CONVERTS_MARKERS)

            if resolve_hits > 0:
                resolve_count += resolve_hits
                resolve_evidence.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label="resolution_resolves",
                    source_session_id=session_id,
                ))
            if open_hits > 0:
                open_count += open_hits
                open_evidence.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label="resolution_leaves_open",
                    source_session_id=session_id,
                ))
            if convert_hits > 0:
                convert_count += convert_hits
                convert_evidence.append(EvidencePassage(
                    passage_text=sent.strip(),
                    passage_index=idx,
                    label="resolution_converts",
                    source_session_id=session_id,
                ))

        # Determine dominant resolution type
        counts = {
            ResolutionPatternType.RESOLVES: resolve_count,
            ResolutionPatternType.LEAVES_OPEN: open_count,
            ResolutionPatternType.CONVERTS: convert_count,
        }
        total = sum(counts.values())
        resolution = ResolutionPattern()

        if total > 0:
            dominant_type = max(counts, key=lambda k: counts[k])
            resolution.dominant = dominant_type
            resolution.evidence_passages = (
                resolve_evidence[:3] + open_evidence[:3] + convert_evidence[:3]
            )

        # Emotional bleed signatures
        bleed_signatures: list[EmotionalBleedSignature] = []
        bleed_evidence = _find_sentences_with_patterns(
            sentences, BLEED_MARKERS, "bleed_signature", session_id
        )

        for ev in bleed_evidence:
            # Try to identify the two emotions involved
            emotions = self._identify_bleed_emotions(ev.passage_text)
            if emotions:
                bleed_signatures.append(EmotionalBleedSignature(
                    primary_emotion=emotions[0],
                    bleeds_into=emotions[1],
                    trigger_context=ev.passage_text[:150],
                    construction_marker=self._identify_bleed_marker(ev.passage_text),
                    evidence_passages=[ev],
                ))

        return resolution, bleed_signatures

    # ──────────────────────────────────────────────────────────
    # Helper Methods
    # ──────────────────────────────────────────────────────────

    def _score_emotional_intensity(self, text: str) -> int:
        """Score emotional intensity of a text passage (0-10)."""
        score = 0

        # All-register emotional keywords
        total_emotion_hits = 0
        for _register, patterns in EMOTIONAL_REGISTERS.items():
            total_emotion_hits += _count_matches(text, patterns)
        score += min(5, total_emotion_hits)

        # Exclamation marks
        score += min(2, text.count("!"))

        # ALL CAPS words
        caps_words = re.findall(r"\b[A-Z]{3,}\b", text)
        score += min(2, len(caps_words))

        # Intensifiers
        intensifiers = re.findall(
            r"\b(very|extremely|absolutely|totally|utterly|incredibly|deeply)\b",
            text, re.IGNORECASE,
        )
        score += min(1, len(intensifiers))

        return min(10, score)

    def _intensity_to_ttt(self, intensity: int) -> str:
        """Map intensity score to Text-Thermometer-Type label."""
        if intensity >= 7:
            return "HIGH"
        elif intensity >= 4:
            return "MEDIUM"
        else:
            return "LOW"

    def _identify_construction(self, text: str) -> str:
        """Identify the linguistic construction signature at ceiling.

        e.g., 'rhetorical question', 'imperative', 'personal testimony'.
        """
        if "?" in text:
            return "rhetorical_question"
        if re.search(r"^(Do|Stop|Start|Go|Don't|Never)", text):
            return "imperative"
        if re.search(r"\b(I |my |me |mine)\b", text, re.IGNORECASE):
            return "personal_testimony"
        if re.search(r"\b(we |our |us )\b", text, re.IGNORECASE):
            return "collective_appeal"
        return "declarative"

    def _identify_active_emotion(self, text: str) -> str:
        """Identify the most active emotional register in text."""
        best_register = "unclassified"
        best_count = 0

        for register, patterns in EMOTIONAL_REGISTERS.items():
            count = _count_matches(text, patterns)
            if count > best_count:
                best_count = count
                best_register = register

        return best_register

    def _identify_bleed_emotions(self, text: str) -> list[str]:
        """Identify the two emotions in a bleed-between-registers passage.

        Returns [primary_emotion, bleeds_into] or empty list.
        """
        found: list[str] = []
        for register, patterns in EMOTIONAL_REGISTERS.items():
            if _count_matches(text, patterns) > 0:
                found.append(register)
            if len(found) >= 2:
                break

        return found if len(found) >= 2 else []

    def _identify_bleed_marker(self, text: str) -> str:
        """Identify the linguistic marker of emotion bleed.

        e.g., 'but actually I'm', 'no — I'm', 'wait, I'm'.
        """
        for pattern in BLEED_MARKERS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return "implicit_transition"
