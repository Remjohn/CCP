"""
src/ccp/services/benchmark_profile_services.py
==============================================
Canonical services for benchmark profile management, archetype overlays, and card weighting calculations.
"""

from __future__ import annotations
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

from src.ccp.models.benchmark_profile_models import (
    ContentType,
    CardRole,
    VisibleScoreKey,
    VisibleScoreWeightMap,
    PenaltyAdjustmentMap,
    ModalityDimension,
    ModalitySupportProfile,
    ContentBenchmarkProfile,
    ScoreEmphasis,
    ArchetypeScoreBundle,
    CardWeightingBundle,
    OverallScoreComputation,
    SINGLE_IMAGE_BASELINE,
    CAROUSEL_BASELINE,
    REEL_BASELINE
)
from src.ccp.models.archetype_container_runtime_models import ArchetypeChoice
from src.ccp.core.receipt_chain import ReceiptChain, ReceiptEntry
from src.ccp.models.eval_registry_models import VisibleFamilyKey

logger = logging.getLogger("ccp.benchmark_profile_services")


class BenchmarkProfileRegistry:
    """Manages content-type-specific benchmark profiles with Supabase integration and in-memory fallbacks."""

    def __init__(
        self,
        supabase_client: Optional[Any] = None,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "SYS"
    ):
        self.supabase = supabase_client
        self.coach_acronym = coach_acronym
        self._receipt_chain = receipt_chain
        
        # In-memory registry for baseline profiles
        self._registry: Dict[ContentType, ContentBenchmarkProfile] = {
            ContentType.SINGLE_IMAGE_POST: SINGLE_IMAGE_BASELINE,
            ContentType.CAROUSEL: CAROUSEL_BASELINE,
            ContentType.REEL: REEL_BASELINE,
        }

    @property
    def receipt_chain(self) -> ReceiptChain:
        if self._receipt_chain is None:
            self._receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym, supabase_client=self.supabase)
        return self._receipt_chain

    def register_profile(self, profile: ContentBenchmarkProfile) -> None:
        """Registers a profile in-memory and attempts persistence in Supabase."""
        self._registry[profile.content_type] = profile
        if self.supabase:
            try:
                self.supabase.table("benchmark_profiles").upsert({
                    "profile_id": profile.profile_id,
                    "profile_version": profile.profile_version,
                    "content_type": profile.content_type.value,
                    "profile_json": profile.model_dump(),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }).execute()
            except Exception as e:
                logger.error(f"Failed to persist profile {profile.profile_id} to Supabase: {e}")

    def resolve_profile(self, content_type: ContentType) -> ContentBenchmarkProfile:
        """Resolves a profile from Supabase or in-memory baselines, with a safe equal-weight fallback."""
        if not isinstance(content_type, ContentType):
            try:
                content_type = ContentType(content_type)
            except ValueError:
                raise ValueError(f"Unknown ContentType: {content_type}")

        # 1. Try Supabase
        if self.supabase:
            try:
                res = self.supabase.table("benchmark_profiles") \
                    .select("*") \
                    .eq("content_type", content_type.value) \
                    .order("created_at", desc=True) \
                    .limit(1) \
                    .execute()
                if res and getattr(res, "data", None):
                    row = res.data[0]
                    profile_json = row.get("profile_json")
                    if profile_json:
                        return ContentBenchmarkProfile.model_validate(profile_json)
            except Exception as e:
                logger.warning(f"Supabase lookup failed for benchmark profile of type {content_type.value}: {e}")

        # 2. Try In-memory registry
        if content_type in self._registry:
            return self._registry[content_type]

        # 3. Fallback to equal-weight baseline (6.1)
        fallback_weights = VisibleScoreWeightMap(
            humanity=0.167,
            presence=0.167,
            trust=0.167,
            memorability=0.167,
            resonance=0.166,
            signal=0.166
        )
        fallback_profile = ContentBenchmarkProfile(
            profile_id="CBP-FALLBACK",
            profile_version="1.0",
            content_type=content_type,
            base_weights=fallback_weights,
            penalties=PenaltyAdjustmentMap(),
            modality_profile=ModalitySupportProfile(
                modality_id="MOD-FALLBACK",
                content_type=content_type,
                dimensions=[
                    ModalityDimension(
                        dimension_id="FALLBACK-D1",
                        dimension_name="generic_fallback_dimension",
                        feeds_cluster="structure",
                        weight_in_cluster=1.0
                    )
                ]
            ),
            rationale="FALLBACK: equal-weight baseline used because no registered profile matches this content type."
        )

        # Log fallback to receipt chain
        self.receipt_chain.log(
            agent_id="BenchmarkProfileRegistry",
            action="benchmark_profile_fallback",
            asset_id=content_type.value,
            input_summary=f"Resolve profile for {content_type.value}",
            output_summary="FALLBACK: equal-weight baseline used",
            decision="fallback",
            decision_rationale=f"No profile registered for content type '{content_type.value}'",
            metadata={"content_type": content_type.value}
        )

        return fallback_profile


class ArchetypeBundleResolver:
    """Manages archetype-specific score emphasis and penalty bundles with Supabase and in-memory fallbacks."""

    def __init__(
        self,
        supabase_client: Optional[Any] = None,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "SYS"
    ):
        self.supabase = supabase_client
        self.coach_acronym = coach_acronym
        self._receipt_chain = receipt_chain
        
        # In-memory store keyed by (archetype, content_type)
        self._registry: Dict[tuple[ArchetypeChoice, ContentType], ArchetypeScoreBundle] = {}

    @property
    def receipt_chain(self) -> ReceiptChain:
        if self._receipt_chain is None:
            self._receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym, supabase_client=self.supabase)
        return self._receipt_chain

    def register_bundle(self, bundle: ArchetypeScoreBundle) -> None:
        """Registers an ArchetypeScoreBundle in-memory and attempts persistence in Supabase."""
        self._registry[(bundle.archetype_choice, bundle.content_type)] = bundle
        if self.supabase:
            try:
                self.supabase.table("archetype_score_bundles").upsert({
                    "bundle_id": bundle.bundle_id,
                    "archetype_choice": bundle.archetype_choice.value,
                    "content_type": bundle.content_type.value,
                    "bundle_json": bundle.model_dump(),
                    "created_at": datetime.now(timezone.utc).isoformat()
                }).execute()
            except Exception as e:
                logger.error(f"Failed to persist archetype bundle {bundle.bundle_id} to Supabase: {e}")

    def resolve_bundle(self, archetype: ArchetypeChoice, content_type: ContentType) -> Optional[ArchetypeScoreBundle]:
        """Resolves an archetype bundle, returning None and logging a fallback warning if absent."""
        if not isinstance(archetype, ArchetypeChoice):
            archetype = ArchetypeChoice(archetype)
        if not isinstance(content_type, ContentType):
            content_type = ContentType(content_type)

        # 1. Try Supabase
        if self.supabase:
            try:
                res = self.supabase.table("archetype_score_bundles") \
                    .select("*") \
                    .eq("archetype_choice", archetype.value) \
                    .eq("content_type", content_type.value) \
                    .order("created_at", desc=True) \
                    .limit(1) \
                    .execute()
                if res and getattr(res, "data", None):
                    row = res.data[0]
                    bundle_json = row.get("bundle_json")
                    if bundle_json:
                        return ArchetypeScoreBundle.model_validate(bundle_json)
            except Exception as e:
                logger.warning(f"Supabase lookup failed for archetype bundle ({archetype.value}, {content_type.value}): {e}")

        # 2. Try In-memory registry
        key = (archetype, content_type)
        if key in self._registry:
            return self._registry[key]

        # 3. Fallback: log warning and return None (6.2)
        self.receipt_chain.log(
            agent_id="ArchetypeBundleResolver",
            action="archetype_bundle_fallback",
            asset_id=f"{archetype.value}:{content_type.value}",
            input_summary=f"Resolve archetype overlay for archetype {archetype.value} and content type {content_type.value}",
            output_summary="FALLBACK: no archetype overlay applied",
            decision="fallback",
            decision_rationale=f"No archetype score bundle registered for {archetype.value} on {content_type.value}",
            metadata={"archetype": archetype.value, "content_type": content_type.value}
        )

        return None


class CardWeightingResolver:
    """Calculates final weight distributions by merging baseline profiles and archetype overlays."""

    def __init__(
        self,
        profile_registry: BenchmarkProfileRegistry,
        bundle_resolver: ArchetypeBundleResolver,
        supabase_client: Optional[Any] = None,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "SYS"
    ):
        self.profile_registry = profile_registry
        self.bundle_resolver = bundle_resolver
        self.supabase = supabase_client
        self.coach_acronym = coach_acronym
        self._receipt_chain = receipt_chain

    @property
    def receipt_chain(self) -> ReceiptChain:
        if self._receipt_chain is None:
            self._receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym, supabase_client=self.supabase)
        return self._receipt_chain

    def resolve_card_weights(
        self,
        content_type: ContentType,
        archetype: ArchetypeChoice,
        card_role: CardRole
    ) -> CardWeightingBundle:
        """Resolves, overlays, renormalizes, and traces the final CardWeightingBundle."""
        # 1. Resolve core components
        profile = self.profile_registry.resolve_profile(content_type)
        bundle = self.bundle_resolver.resolve_bundle(archetype, content_type)

        # 2. Extract baseline weights
        base_weights = profile.base_weights
        weights_dict = {
            "humanity": base_weights.humanity,
            "presence": base_weights.presence,
            "trust": base_weights.trust,
            "memorability": base_weights.memorability,
            "resonance": base_weights.resonance,
            "signal": base_weights.signal
        }

        trace_log = []
        source_bundle_id = "NONE"

        # 3. Apply archetype score emphasis overlay
        if bundle:
            source_bundle_id = bundle.bundle_id
            trace_log.append(f"Overlay applied from bundle {bundle.bundle_id}.")
            for adj in bundle.emphasis_adjustments:
                k = adj.score_key.value
                if k in weights_dict:
                    old_val = weights_dict[k]
                    weights_dict[k] += adj.emphasis_delta
                    weights_dict[k] = max(0.0, min(1.0, weights_dict[k]))
                    trace_log.append(f"Shifted {k}: {old_val:.4f} -> {weights_dict[k]:.4f} (delta: {adj.emphasis_delta})")
        else:
            trace_log.append("No archetype overlay bundle found. Using baseline weights.")

        # 4. Enforce sum-to-1.0 and handle renormalization (6.4)
        original_sum = sum(weights_dict.values())
        drift_detected = not (0.99 <= original_sum <= 1.01)

        # Always renormalize to be precisely mathematically sound
        if original_sum > 0:
            for k in weights_dict:
                weights_dict[k] /= original_sum
        else:
            # Emergency equal weight distribution fallback
            for k in weights_dict:
                weights_dict[k] = 1.0 / 6.0

        resolved_weights = VisibleScoreWeightMap(**weights_dict)

        if drift_detected:
            trace_log.append(f"Renormalized weights due to sum drift: {original_sum:.4f} -> 1.0000")
            # Log weight_renormalized to receipt chain
            self.receipt_chain.log(
                agent_id="CardWeightingResolver",
                action="weight_renormalized",
                asset_id=f"{archetype.value}:{content_type.value}:{card_role.value}",
                input_summary=f"Renormalize weights after applying deltas. Original sum: {original_sum:.4f}",
                output_summary="Renormalization complete",
                decision="renormalized",
                decision_rationale=f"Archetype adjustments caused weights to sum to {original_sum:.4f}, violating the 1.0 contract.",
                metadata={
                    "original_sum": original_sum,
                    "normalized_weights": weights_dict
                }
            )

        # 5. Resolve penalties (archetype bundle overrides take precedence)
        resolved_penalties = profile.penalties
        if bundle and bundle.penalty_overrides:
            resolved_penalties = bundle.penalty_overrides
            trace_log.append("Applied archetype-specific penalty overrides.")
        else:
            trace_log.append("Applied profile baseline penalties.")

        # 6. Extract modality dimensions
        modality_dimensions = profile.modality_profile.dimensions if profile.modality_profile else []

        # 7. Construct Resolved CardWeightingBundle
        resolved_bundle = CardWeightingBundle(
            bundle_id=f"CWB-{uuid.uuid4().hex[:8].upper()}",
            content_type=content_type,
            archetype_choice=archetype,
            card_role=card_role,
            resolved_weights=resolved_weights,
            resolved_penalties=resolved_penalties,
            modality_dimensions=modality_dimensions,
            source_profile_id=profile.profile_id,
            source_bundle_id=source_bundle_id,
            resolution_trace=" | ".join(trace_log)
        )

        # 8. Persistence to Supabase
        if self.supabase:
            try:
                self.supabase.table("card_weighting_bundles").insert({
                    "bundle_id": resolved_bundle.bundle_id,
                    "content_type": resolved_bundle.content_type.value,
                    "archetype_choice": resolved_bundle.archetype_choice.value,
                    "card_role": resolved_bundle.card_role.value,
                    "resolved_json": resolved_bundle.model_dump(),
                    "source_profile_id": resolved_bundle.source_profile_id,
                    "source_bundle_id": resolved_bundle.source_bundle_id,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }).execute()
            except Exception as e:
                logger.error(f"Failed to persist resolved card weighting bundle {resolved_bundle.bundle_id}: {e}")

        # 9. Log resolved event to receipt chain
        self.receipt_chain.log(
            agent_id="CardWeightingResolver",
            action="card_weights_resolved",
            asset_id=resolved_bundle.bundle_id,
            input_summary=f"Resolve card weighting for {content_type.value} + {archetype.value} for role {card_role.value}",
            output_summary=f"Weights resolved. Rationale trace: {resolved_bundle.resolution_trace}",
            decision="resolved",
            decision_rationale="Successfully calculated weighting bundle matching content constraints and archetype emphasis.",
            metadata=resolved_bundle.model_dump()
        )

        return resolved_bundle


class OverallScoreCalculator:
    """Calculates final scores by weighting inputs, applying slop risk penalties, and enforcing governance caps."""

    def __init__(
        self,
        supabase_client: Optional[Any] = None,
        receipt_chain: Optional[ReceiptChain] = None,
        coach_acronym: str = "SYS"
    ):
        self.supabase = supabase_client
        self.coach_acronym = coach_acronym
        self._receipt_chain = receipt_chain

    @property
    def receipt_chain(self) -> ReceiptChain:
        if self._receipt_chain is None:
            self._receipt_chain = ReceiptChain(coach_acronym=self.coach_acronym, supabase_client=self.supabase)
        return self._receipt_chain

    def compute_overall(
        self,
        raw_scores: Dict[str, float],
        card_weighting_bundle: CardWeightingBundle
    ) -> OverallScoreComputation:
        """Computes the final, governed overall score using a resolved CardWeightingBundle."""
        # 1. Normalize input keys to lower_case for seamless interop with Title Case enums
        norm_raw = {}
        for k, v in raw_scores.items():
            norm_key = str(k).lower().strip().replace(" ", "_")
            # If the user passed it as a Title Case Enum name or value (e.g. VisibleFamilyKey.AI_SLOP_RISK.value)
            if norm_key == "ai_slop_risk":
                norm_raw["ai_slop_risk"] = float(v)
            else:
                norm_raw[norm_key] = float(v)

        w = card_weighting_bundle.resolved_weights
        penalties = card_weighting_bundle.resolved_penalties

        # 2. Compute weighted base score (0.0 to 100.0)
        weighted_base = (
            norm_raw.get("humanity", 0.0) * w.humanity +
            norm_raw.get("presence", 0.0) * w.presence +
            norm_raw.get("trust", 0.0) * w.trust +
            norm_raw.get("memorability", 0.0) * w.memorability +
            norm_raw.get("resonance", 0.0) * w.resonance +
            norm_raw.get("signal", 0.0) * w.signal
        )

        trace_log = [f"Weighted base calculated: {weighted_base:.2f}"]

        # 3. Compute and apply AI Slop Risk penalty (if risk score present)
        slop_val = norm_raw.get("ai_slop_risk", 0.0)
        slop_penalty_applied = slop_val * penalties.ai_slop_penalty_multiplier
        overall_score = max(0.0, weighted_base - slop_penalty_applied)
        trace_log.append(f"AI Slop Risk ({slop_val:.1f}) applied penalty of {slop_penalty_applied:.2f} (multiplier: {penalties.ai_slop_penalty_multiplier:.2f}). Interim overall: {overall_score:.2f}")

        # 4. Process and enforce governance caps (applying strictest/minimum cap)
        caps_applied = []
        caps_values = []

        # Trust Floor Cap
        trust_val = norm_raw.get("trust", 0.0)
        if trust_val < penalties.trust_floor:
            caps_values.append(penalties.overall_cap_when_trust_below_floor)
            caps_applied.append("trust_floor_cap")
            trace_log.append(f"Trust ({trust_val:.1f}) below floor ({penalties.trust_floor:.1f}) triggers cap limit of {penalties.overall_cap_when_trust_below_floor:.1f}")

        # Humanity Floor Cap
        humanity_val = norm_raw.get("humanity", 0.0)
        if humanity_val < penalties.humanity_floor:
            caps_values.append(penalties.overall_cap_when_humanity_below_floor)
            caps_applied.append("humanity_floor_cap")
            trace_log.append(f"Humanity ({humanity_val:.1f}) below floor ({penalties.humanity_floor:.1f}) triggers cap limit of {penalties.overall_cap_when_humanity_below_floor:.1f}")

        # Slop Danger Cap
        if slop_val > penalties.slop_danger_threshold:
            caps_values.append(penalties.overall_cap_when_slop_above_threshold)
            caps_applied.append("slop_danger_cap")
            trace_log.append(f"AI Slop Risk ({slop_val:.1f}) exceeds danger threshold ({penalties.slop_danger_threshold:.1f}) triggers cap limit of {penalties.overall_cap_when_slop_above_threshold:.1f}")

        # Presence Without Trust Cap (AC-BEN-6)
        presence_val = norm_raw.get("presence", 0.0)
        if trust_val < penalties.trust_floor and presence_val > penalties.presence_without_trust_cap:
            caps_values.append(penalties.presence_without_trust_cap)
            caps_applied.append("presence_without_trust_cap")
            trace_log.append(f"High Presence ({presence_val:.1f}) without Trust triggers 'presence_without_trust_cap' of {penalties.presence_without_trust_cap:.1f}")

        # Apply strict minimum cap if any caps triggered
        if caps_values:
            strictest_cap = min(caps_values)
            overall_before_cap = overall_score
            overall_score = min(overall_score, strictest_cap)
            trace_log.append(f"Governance caps applied. Strictest cap: {strictest_cap:.1f}. Score capped: {overall_before_cap:.2f} -> {overall_score:.2f}")

        # Bounds checks: final overall must be in [0, 99] (as integer)
        final_overall_score = max(0, min(99, int(overall_score)))
        trace_log.append(f"Final overall score bounded and cast: {final_overall_score}")

        computation = OverallScoreComputation(
            raw_scores=raw_scores,
            card_weighting_bundle=card_weighting_bundle,
            weighted_base=weighted_base,
            slop_penalty_applied=slop_penalty_applied,
            caps_applied=caps_applied,
            final_overall=final_overall_score,
            computation_trace=" | ".join(trace_log)
        )

        # 5. Log resolved event to receipt chain
        self.receipt_chain.log(
            agent_id="OverallScoreCalculator",
            action="overall_score_computed",
            asset_id=card_weighting_bundle.bundle_id,
            input_summary=f"Compute overall score for raw input map containing {len(raw_scores)} entries.",
            output_summary=f"Final score: {final_overall_score}. Caps: {caps_applied}",
            decision="computed",
            decision_rationale=computation.computation_trace,
            metadata=computation.model_dump()
        )

        return computation
