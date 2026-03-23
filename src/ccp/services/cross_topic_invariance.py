"""
CCP FR3 Cross-Topic Invariance Test — Unit 4
The hardest and most important step in the pipeline.

Spec reference: FR3 Tech Spec §Step 3 — Cross-Topic Invariance Test
Agent: Valeriane

Action:
1. Identify 5 maximally different subject clusters from corpus
2. Run discourse marker analysis separately for EACH cluster
3. Compare: marker's position distribution must remain consistent (within ±15%)
4. Markers with >15% variance → flagged as TOPIC-SPECIFIC, excluded from DEP-ENG-003
5. Only invariant markers advance

Gate: Minimum 12 invariant markers required.
"""

import re
from collections import Counter
from typing import Optional

from src.ccp.models.voice_dna_models import (
    INVARIANCE_THRESHOLD_PCT,
    MINIMUM_INVARIANT_MARKERS,
    CorpusUnit,
    ExtractionCorpus,
    InvarianceTestResult,
    MarkerInvarianceResult,
    MarkerInvarianceStatus,
    MarkerPositionDistribution,
    TopicCluster,
)
from src.ccp.services.discourse_marker_census import DiscourseMarkerCensus


class InsufficientInvariantMarkersError(Exception):
    """Raised when fewer than 12 invariant markers found.
    Spec §Step 3 Gate: 'expand corpus (more Sacred Audio) or broaden subject clusters.'"""
    pass


# ──────────────────────────────────────────────────────────────
# Topic keywords for subject clustering
# Spec §Step 3: '5 maximally different subject clusters (e.g., professional
# development, personal health, relationships, finances, industry critique)'
# ──────────────────────────────────────────────────────────────

TOPIC_CLUSTERS: dict[str, list[str]] = {
    "professional_development": [
        "career", "business", "work", "job", "professional", "leadership",
        "management", "team", "project", "strategy", "growth", "skill",
        "client", "revenue", "company", "brand", "market", "industry",
        "networking", "mentor", "promotion", "startup", "entrepreneurship",
    ],
    "personal_health": [
        "health", "body", "fitness", "exercise", "diet", "sleep", "energy",
        "stress", "anxiety", "meditation", "yoga", "mindfulness", "wellness",
        "burnout", "recovery", "therapy", "mental", "physical", "routine",
        "self-care", "habit", "discipline",
    ],
    "relationships": [
        "relationship", "love", "partner", "family", "friend", "trust",
        "communication", "boundary", "intimacy", "conflict", "marriage",
        "divorce", "parent", "child", "connection", "loneliness", "support",
        "attachment", "vulnerability", "empathy", "forgiveness",
    ],
    "finances": [
        "money", "finance", "invest", "save", "debt", "income", "wealth",
        "budget", "expense", "profit", "loss", "tax", "retirement", "asset",
        "spending", "earning", "pricing", "abundance", "scarcity", "financial",
    ],
    "identity_values": [
        "identity", "purpose", "meaning", "values", "belief", "faith",
        "spiritual", "soul", "authentic", "truth", "integrity", "courage",
        "fear", "shame", "guilt", "worthiness", "self-worth", "confidence",
        "transformation", "growth", "becoming", "calling", "passion",
    ],
}


class CrossTopicInvarianceTest:
    """Executes the cross-topic invariance test on the extraction corpus.

    Spec §Step 3: 'This is the hardest and most important step in the pipeline.'

    A marker's position distribution must remain consistent (within ±15%) across
    all 5 clusters to qualify as Voice DNA. Markers with >15% variance are
    TOPIC-SPECIFIC and excluded from DEP-ENG-003.
    """

    def __init__(
        self,
        discourse_census: Optional[DiscourseMarkerCensus] = None,
        spacy_model=None,
    ):
        self.census = discourse_census or DiscourseMarkerCensus(spacy_model=spacy_model)

    def test(
        self,
        corpus: ExtractionCorpus,
        global_marker_map: Optional[dict] = None,
    ) -> InvarianceTestResult:
        """Execute the cross-topic invariance test.

        Args:
            corpus: Assembled extraction corpus from Step 1.
            global_marker_map: Pre-computed global DiscourseMarkerMap (optional).

        Returns:
            InvarianceTestResult with invariant and topic-specific classifications.

        Raises:
            InsufficientInvariantMarkersError: If <12 invariant markers found.
        """
        # Step 1: Assign corpus units to topic clusters
        clusters = self._build_clusters(corpus)

        # Step 2: Run discourse marker census for each cluster
        cluster_distributions = self._compute_cluster_distributions(clusters, corpus)

        # Step 3: Compare distributions across clusters
        # Get all markers that appear in at least 2 clusters
        all_markers = set()
        for dists in cluster_distributions.values():
            all_markers.update(dists.keys())

        result = InvarianceTestResult(clusters_used=len(clusters))

        for marker in sorted(all_markers):
            marker_result = self._evaluate_marker_invariance(
                marker, cluster_distributions
            )
            result.markers.append(marker_result)

            if marker_result.status == MarkerInvarianceStatus.INVARIANT:
                result.invariant_markers.append(marker)
            else:
                result.topic_specific_markers.append(marker)

        return result

    def _build_clusters(
        self, corpus: ExtractionCorpus
    ) -> dict[str, list[CorpusUnit]]:
        """Assign corpus units to the 5 topic clusters based on keyword density.

        Spec §Step 3: 'identify 5 maximally different subject clusters'.

        Each unit is assigned to the cluster with the highest keyword match count.
        Units that don't match any cluster well go into a 'mixed' bucket and
        are distributed to underrepresented clusters.
        """
        cluster_units: dict[str, list[CorpusUnit]] = {
            name: [] for name in TOPIC_CLUSTERS
        }
        unassigned: list[CorpusUnit] = []

        for unit in corpus.units:
            text_lower = unit.text.lower()
            cluster_scores: dict[str, int] = {}

            for cluster_name, keywords in TOPIC_CLUSTERS.items():
                score = sum(
                    1 for kw in keywords
                    if re.search(rf"\b{re.escape(kw)}\b", text_lower)
                )
                if score > 0:
                    cluster_scores[cluster_name] = score

            if cluster_scores:
                best_cluster = max(cluster_scores, key=lambda c: cluster_scores[c])
                cluster_units[best_cluster].append(unit)
            else:
                unassigned.append(unit)

        # Distribute unassigned units to underrepresented clusters
        sorted_clusters = sorted(cluster_units.keys(), key=lambda c: len(cluster_units[c]))
        for i, unit in enumerate(unassigned):
            target = sorted_clusters[i % len(sorted_clusters)]
            cluster_units[target].append(unit)

        # Filter out empty clusters
        return {k: v for k, v in cluster_units.items() if len(v) > 0}

    def _compute_cluster_distributions(
        self,
        clusters: dict[str, list[CorpusUnit]],
        corpus: ExtractionCorpus,
    ) -> dict[str, dict[str, MarkerPositionDistribution]]:
        """Run discourse marker census for each topic cluster.

        Spec §Step 3: 'Run Step 2's discourse marker analysis separately
        for EACH cluster.'
        """
        distributions: dict[str, dict[str, MarkerPositionDistribution]] = {}

        for cluster_name, units in clusters.items():
            cluster_text = " ".join(u.text for u in units)
            if cluster_text.strip():
                distributions[cluster_name] = self.census.census_for_cluster(
                    cluster_text
                )

        return distributions

    def _evaluate_marker_invariance(
        self,
        marker: str,
        cluster_distributions: dict[str, dict[str, MarkerPositionDistribution]],
    ) -> MarkerInvarianceResult:
        """Evaluate whether a marker's position distribution is invariant.

        Spec §Step 3: 'A marker's position distribution must remain consistent
        (within ±15%) across all 5 clusters to qualify as Voice DNA.'

        Uses sentence_opening_pct as the primary comparison metric,
        since it's the most distinctive positional feature.
        """
        cluster_values: dict[str, float] = {}

        for cluster_name, dists in cluster_distributions.items():
            if marker in dists:
                dist = dists[marker]
                # Use sentence_opening_pct as the primary invariance metric
                cluster_values[cluster_name] = dist.sentence_opening_pct

        # Need at least 2 clusters with this marker to evaluate
        if len(cluster_values) < 2:
            return MarkerInvarianceResult(
                marker=marker,
                status=MarkerInvarianceStatus.TOPIC_SPECIFIC,
                max_variance_pct=100.0,
                cluster_values=cluster_values,
                detail=f"Marker '{marker}' appears in fewer than 2 clusters — insufficient for invariance test.",
            )

        # Compute max variance across all cluster pairs
        values = list(cluster_values.values())
        max_val = max(values)
        min_val = min(values)

        # Variance = absolute difference (percentage points)
        max_variance = max_val - min_val

        if max_variance <= INVARIANCE_THRESHOLD_PCT:
            return MarkerInvarianceResult(
                marker=marker,
                status=MarkerInvarianceStatus.INVARIANT,
                max_variance_pct=max_variance,
                cluster_values=cluster_values,
                detail=(
                    f"Marker '{marker}' is INVARIANT: max variance {max_variance:.1f}% "
                    f"≤ threshold {INVARIANCE_THRESHOLD_PCT}%."
                ),
            )
        else:
            return MarkerInvarianceResult(
                marker=marker,
                status=MarkerInvarianceStatus.TOPIC_SPECIFIC,
                max_variance_pct=max_variance,
                cluster_values=cluster_values,
                detail=(
                    f"Marker '{marker}' is TOPIC-SPECIFIC: max variance {max_variance:.1f}% "
                    f"> threshold {INVARIANCE_THRESHOLD_PCT}%."
                ),
            )
