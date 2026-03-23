"""
CCP FR3 Positive Space Extraction + Humor Classification — Unit 7
Transforms the 5 stylometry clusters into DEP-ENG-003 with prose descriptions.

Spec reference: FR3 Tech Spec §Steps 6-8 — Positive Space Extraction (DEP-ENG-003)
Agent: Valeriane

Prerequisite gate: DEP-ENG-004 must exist (Mandate 4 — hardcoded, not a prompt instruction)

Actions:
  Steps 6-7: For each of the 5 stylometry clusters → numerical profile + prose description
  Step 8: Humor Style Classification (Mandate 8 input)

The prose description is what the generation agent reads — it translates the
mathematical profile into a voice instruction for Block A of compiled SKILL.md files.
"""

import re
from collections import Counter
from typing import Optional

from src.ccp.models.voice_dna_models import (
    ClusterProseDescription,
    ExtractionCorpus,
    HumorStyleClassification,
    HumorType,
    NegativeSpaceObject,
    PositiveSpaceObject,
    StylometryProfile,
)


class Mandate4GateError(Exception):
    """Raised when DEP-ENG-004 is not present.
    Spec §Step 6: 'Prerequisite gate: DEP-ENG-004 exists in coach_soul.json'
    AC2: 'the pipeline halts with a DEP-ENG-004_NOT_FOUND error
    (not a prompt failure — a code-level gate)'."""
    pass


class IncompletePositiveSpaceError(Exception):
    """Raised when DEP-ENG-003 is incomplete (not all 5 clusters have prose).
    Stress test Q2: 'An incomplete matrix evaluates as status: PARTIAL → FALSE.'"""
    pass


class PositiveSpaceExtractor:
    """Extracts DEP-ENG-003 (Positive Space Object) + humor classification.

    Spec §Steps 6-8: 'For each cluster, generate the numerical profile AND
    a prose description suitable for inclusion in Block A of compiled SKILL.md files.'

    Mandate 4 enforcement: Will not proceed without a validated DEP-ENG-004.
    """

    def extract(
        self,
        stylometry_profile: StylometryProfile,
        negative_space: Optional[NegativeSpaceObject] = None,
        corpus: Optional[ExtractionCorpus] = None,
    ) -> tuple[PositiveSpaceObject, Optional[HumorStyleClassification]]:
        """Execute Steps 6-8: Positive Space Extraction + Humor Classification.

        Args:
            stylometry_profile: StylometryProfile from Step 4.
            negative_space: DEP-ENG-004 from Step 5 (required for Mandate 4 gate).
            corpus: Original corpus for humor analysis (Step 8).

        Returns:
            Tuple of (PositiveSpaceObject, HumorStyleClassification or None).

        Raises:
            Mandate4GateError: If DEP-ENG-004 is not provided or empty.
            IncompletePositiveSpaceError: If any cluster lacks a prose description.
        """
        # ── Mandate 4 Gate (hardcoded) ──
        if negative_space is None:
            raise Mandate4GateError(
                "DEP-ENG-004_NOT_FOUND: Negative Space Object must be produced "
                "before Positive Space extraction can begin. This is a code-level "
                "gate enforcing Mandate 4 (Negative Space Before Positive Space)."
            )

        if negative_space.total_contrastive_strings() == 0:
            raise Mandate4GateError(
                "DEP-ENG-004_EMPTY: Negative Space Object exists but contains "
                "zero contrastive strings. Cannot proceed with Positive Space "
                "extraction until DEP-ENG-004 is populated."
            )

        # ── Steps 6-7: Build cluster prose descriptions ──
        clusters = self._build_cluster_descriptions(stylometry_profile)

        positive_space = PositiveSpaceObject(
            clusters=clusters,
            stylometry_profile=stylometry_profile,
            total_variables=self._count_variables(stylometry_profile),
        )

        # Verify completeness (Stress test Q2)
        if not positive_space.is_complete():
            raise IncompletePositiveSpaceError(
                "DEP-ENG-003 is incomplete: not all 5 clusters have prose descriptions. "
                "Status: PARTIAL → pipeline terminates. "
                "More Sacred Audio or broader stylometry analysis required."
            )

        positive_space.compute_hash()

        # ── Step 8: Humor Style Classification ──
        humor = None
        if corpus is not None:
            humor = self._classify_humor_style(corpus)

        return positive_space, humor

    def _build_cluster_descriptions(
        self, profile: StylometryProfile
    ) -> list[ClusterProseDescription]:
        """Build numerical profile + prose description for each of 5 clusters.

        Spec §Steps 6-7: 'The prose description is what the generation agent reads —
        it translates the mathematical profile into a voice instruction.'
        """
        clusters: list[ClusterProseDescription] = []

        # Cluster 1: Lexical/Morphological
        lex = profile.lexical
        lex_prose = self._generate_lexical_prose(lex)
        clusters.append(ClusterProseDescription(
            cluster_name="Lexical/Morphological",
            numerical_profile=lex.model_dump(),
            prose_description=lex_prose,
        ))

        # Cluster 2: Subconscious Syntactic Distributions
        syn = profile.syntactic
        syn_prose = self._generate_syntactic_prose(syn)
        clusters.append(ClusterProseDescription(
            cluster_name="Subconscious Syntactic Distributions",
            numerical_profile=syn.model_dump(),
            prose_description=syn_prose,
        ))

        # Cluster 3: Relational WAN Metrics
        wan = profile.wan_metrics
        wan_prose = self._generate_wan_prose(wan)
        clusters.append(ClusterProseDescription(
            cluster_name="Relational WAN Metrics",
            numerical_profile=wan.model_dump(),
            prose_description=wan_prose,
        ))

        # Cluster 4: Graphical Habits
        gfx = profile.graphical
        gfx_prose = self._generate_graphical_prose(gfx)
        clusters.append(ClusterProseDescription(
            cluster_name="Graphical Habits",
            numerical_profile=gfx.model_dump(),
            prose_description=gfx_prose,
        ))

        # Cluster 5: Structural Complexity
        struct = profile.structural
        struct_prose = self._generate_structural_prose(struct)
        clusters.append(ClusterProseDescription(
            cluster_name="Structural Complexity",
            numerical_profile=struct.model_dump(),
            prose_description=struct_prose,
        ))

        return clusters

    # ──────────────────────────────────────────────────────────
    # Prose Generation for each Cluster
    # ──────────────────────────────────────────────────────────

    def _generate_lexical_prose(self, lex) -> str:
        """Translate Cluster 1 numerical profile into voice instruction."""
        parts = []

        # TTR interpretation
        if lex.type_token_ratio > 0.6:
            parts.append(
                "This coach uses a diverse vocabulary — rarely repeating the same word. "
                "Aim for varied word choices; avoid repetitive language."
            )
        elif lex.type_token_ratio < 0.3:
            parts.append(
                "This coach deliberately reuses signature words — repetition is a feature, "
                "not a bug. Lean into core vocabulary and repeat key terms."
            )
        else:
            parts.append(
                "This coach uses a moderately varied vocabulary. Mix familiar phrases "
                "with occasional novel word choices."
            )

        # Hapax interpretation
        if lex.hapax_legomena_frequency > 0.5:
            parts.append(
                "High hapax frequency — this coach uses many words exactly once. "
                "Include occasional unique or unexpected word choices."
            )
        elif lex.hapax_legomena_frequency < 0.3:
            parts.append(
                "Low hapax frequency — this coach sticks to a core working vocabulary. "
                "Don't introduce unusual or exotic words."
            )

        return " ".join(parts)

    def _generate_syntactic_prose(self, syn) -> str:
        """Translate Cluster 2 numerical profile into voice instruction."""
        parts = []

        # Dominant conjunction
        conj_map = {
            "and": syn.and_density,
            "but": syn.but_density,
            "so": syn.so_density,
        }
        dominant = max(conj_map, key=lambda c: conj_map[c])

        if dominant == "and":
            parts.append(
                "This coach builds through addition — 'and' is the dominant connector. "
                "Layer ideas with cumulative construction."
            )
        elif dominant == "but":
            parts.append(
                "This coach thinks in contrasts — 'but' is the dominant connector. "
                "Use contrasting pivots to build tension and nuance."
            )
        else:
            parts.append(
                "This coach reasons consequentially — 'so' is the dominant connector. "
                "Build cause-and-effect chains."
            )

        # Clause connective ratio
        if syn.clause_connective_ratio > 0.15:
            parts.append(
                "High clause connective ratio — this coach uses complex, multi-clause "
                "sentences. Don't oversimplify into choppy fragments."
            )
        elif syn.clause_connective_ratio < 0.05:
            parts.append(
                "Low clause connective ratio — this coach favors simple, direct sentences. "
                "Avoid over-complicated clause structures."
            )

        return " ".join(parts)

    def _generate_wan_prose(self, wan) -> str:
        """Translate Cluster 3 numerical profile into voice instruction."""
        parts = []

        if wan.adjacency_pairs:
            top_3 = wan.adjacency_pairs[:3]
            pair_strs = [f"'{a}→{b}'" for a, b, _ in top_3]
            parts.append(
                f"Most common function-word transitions: {', '.join(pair_strs)}. "
                "Replicate these micro-level connective patterns."
            )

        if wan.network_density > 0.3:
            parts.append(
                "Dense word adjacency network — this coach's function words connect "
                "in many different combinations. Allow natural variety."
            )
        elif wan.network_density < 0.1:
            parts.append(
                "Sparse word adjacency network — this coach uses predictable function "
                "word sequences. Maintain consistent connective patterns."
            )

        return " ".join(parts) if parts else "Standard WAN metrics — no distinctive patterns detected."

    def _generate_graphical_prose(self, gfx) -> str:
        """Translate Cluster 4 numerical profile into voice instruction."""
        parts = []

        if gfx.em_dash_per_100_words > 1.0:
            parts.append(
                "Heavy em-dash user — this coach interrupts their own thoughts. "
                "Use em-dashes for interjections and mid-thought pivots."
            )
        elif gfx.em_dash_per_100_words < 0.2:
            parts.append(
                "Rarely uses em-dashes. Avoid them in generated content."
            )

        if gfx.ellipsis_frequency > 0.005:
            parts.append(
                "Uses ellipses to create space and pauses. Include trailing "
                "thoughts and deliberate incompletions."
            )

        if gfx.comma_load_per_sentence > 3.0:
            parts.append(
                "Heavy comma load — this coach builds long, layered sentences "
                "with multiple embedded clauses."
            )
        elif gfx.comma_load_per_sentence < 1.0:
            parts.append(
                "Light comma load — this coach favors short, punchy constructions."
            )

        if gfx.exclamation_frequency > 0.1:
            parts.append(
                "Frequent exclamation marks — this coach is expressive and emphatic. "
                "Include occasional exclamatory emphasis."
            )

        return " ".join(parts) if parts else "Standard punctuation habits — no extreme patterns detected."

    def _generate_structural_prose(self, struct) -> str:
        """Translate Cluster 5 numerical profile into voice instruction."""
        parts = []

        if struct.wps_mean < 10:
            parts.append(
                "Short average sentence length — this coach is concise and punchy. "
                "Keep sentences under 12 words on average."
            )
        elif struct.wps_mean > 20:
            parts.append(
                "Long average sentence length — this coach is a storyteller who "
                "builds expansive, flowing sentences. Don't chop them short."
            )
        else:
            parts.append(
                f"Moderate sentence length (average {struct.wps_mean:.0f} words). "
                "Maintain natural variety."
            )

        if struct.wps_std_dev > 8:
            parts.append(
                "High sentence-length variance — this coach alternates dramatically "
                "between short punches and long flows. Replicate this rhythm."
            )

        if struct.short_sentence_ratio > 0.3:
            parts.append(
                "Frequent short sentences (≤5 words). Use one-liners and fragments "
                "to create impact moments."
            )

        if struct.paragraph_length_variance > 1000:
            parts.append(
                "High paragraph-length variance — this coach mixes brief asides "
                "with extended explorations. Vary content block length."
            )

        return " ".join(parts) if parts else "Standard structural complexity — balanced variety."

    def _count_variables(self, profile: StylometryProfile) -> int:
        """Count total variables across all 5 clusters."""
        count = 0
        for cluster_model in [
            profile.lexical, profile.syntactic, profile.wan_metrics,
            profile.graphical, profile.structural,
        ]:
            dump = cluster_model.model_dump()
            for key, value in dump.items():
                if isinstance(value, (int, float)):
                    count += 1
                elif isinstance(value, dict):
                    count += len(value)
                elif isinstance(value, list):
                    count += 1  # Count the list as one variable
        return count

    # ──────────────────────────────────────────────────────────
    # Step 8: Humor Style Classification (Mandate 8)
    # ──────────────────────────────────────────────────────────

    def _classify_humor_style(
        self, corpus: ExtractionCorpus
    ) -> HumorStyleClassification:
        """Step 8: Analyze humor signals in the coach's corpus.

        Spec §Step 8: 'Classify per Architecture 6 — affiliative/self_enhancing/
        aggressive/self_defeating. Write humor_style_classification to coach_soul.json.'
        """
        full_text = " ".join(u.text for u in corpus.units)
        text_lower = full_text.lower()
        total_words = len(full_text.split()) or 1

        # Self-referential humor frequency
        self_ref_patterns = [
            r"\b(?:I used to|my mistake|I was wrong|I'm the worst|embarrassing|"
            r"I'll admit|I have no idea|I'm terrible at|I can't believe I)\b",
        ]
        self_ref_count = sum(
            len(re.findall(p, text_lower)) for p in self_ref_patterns
        )
        self_ref_freq = self_ref_count / (total_words / 1000)

        # Observational irony frequency
        irony_patterns = [
            r"\b(?:of course|obviously|surprise surprise|imagine that|"
            r"naturally|as expected|funny how|isn't it funny|the irony)\b",
        ]
        irony_count = sum(
            len(re.findall(p, text_lower)) for p in irony_patterns
        )
        irony_freq = irony_count / (total_words / 1000)

        # Self-deprecation frequency
        self_dep_patterns = [
            r"\b(?:I'm no|I'm not the|I suck at|my biggest flaw|"
            r"I'm hopeless|I barely|I struggle with|I failed)\b",
        ]
        self_dep_count = sum(
            len(re.findall(p, text_lower)) for p in self_dep_patterns
        )
        self_dep_freq = self_dep_count / (total_words / 1000)

        # Absurdist references
        absurd_patterns = [
            r"\b(?:imagine.*(?:elephant|unicorn|alien|zombie|martian|dinosaur)|"
            r"what if.*(?:trees could|rocks were|the sky|gravity)|"
            r"plot twist|sounds crazy|bonkers|insane)\b",
        ]
        absurd_count = sum(
            len(re.findall(p, text_lower)) for p in absurd_patterns
        )
        absurd_freq = absurd_count / (total_words / 1000)

        # Aggressive targeting
        aggressive_patterns = [
            r"\b(?:those people|idiots|morons|losers|they're so|"
            r"what kind of person|how stupid|what a joke|pathetic)\b",
        ]
        aggressive_present = any(
            re.search(p, text_lower) for p in aggressive_patterns
        )

        # Determine primary and secondary styles
        scores = {
            HumorType.AFFILIATIVE: irony_freq + self_ref_freq * 0.5,
            HumorType.SELF_ENHANCING: irony_freq + absurd_freq,
            HumorType.AGGRESSIVE: (10.0 if aggressive_present else 0.0),
            HumorType.SELF_DEFEATING: self_dep_freq + self_ref_freq * 0.3,
        }

        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_styles[0][0]
        secondary = sorted_styles[1][0] if sorted_styles[1][1] > 0 else None

        return HumorStyleClassification(
            primary_style=primary,
            secondary_style=secondary,
            self_referential_frequency=self_ref_freq,
            observational_irony_frequency=irony_freq,
            self_deprecation_frequency=self_dep_freq,
            absurdist_frequency=absurd_freq,
            aggressive_targeting_present=aggressive_present,
            detail=(
                f"Primary: {primary.value}, Secondary: {secondary.value if secondary else 'none'}. "
                f"Self-ref: {self_ref_freq:.2f}/1k, Irony: {irony_freq:.2f}/1k, "
                f"Self-dep: {self_dep_freq:.2f}/1k, Absurd: {absurd_freq:.2f}/1k."
            ),
        )
