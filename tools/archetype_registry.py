"""
Archetype Registry Tool
-----------------------
Deterministic router that resolves full archetype metadata by joining
across framework_archetype_map.json, archetype_palettes.json, and
persuasive_angles.json.

This is a TOOL (deterministic Python), not a SKILL (no reasoning required).

Usage:
    from tools.archetype_registry import ArchetypeRegistry

    registry = ArchetypeRegistry("path/to/intelligence_library")
    metadata = registry.resolve_archetype(segment)
    batch    = registry.resolve_batch(segments)
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

logger = logging.getLogger(__name__)


# ─── Data Classes ────────────────────────────────────────────────────

@dataclass
class TTTGravityLayer:
    """A single TTT gravity layer (Base, Accent, or Intuitive)."""
    ttt_level: str
    ttt_name: str
    focus: str


@dataclass
class ResolvedPersuasiveAngle:
    """A fully resolved persuasive angle with operational directives."""
    id: str
    name: str
    psychological_trigger: str
    operational_instruction: str
    construction_constraint: str


@dataclass
class ArchetypeMetadata:
    """
    The complete, resolved archetype metadata payload.
    This is what Script Prompts and the Art Director receive.
    """
    # Identity
    archetype_id: str
    archetype_name: str
    archetype_family: str

    # Framework binding
    framework_id: str
    framework_name: str
    priority_level: int

    # Visual routing
    visual_category: str  # single_frame | comparison | sequential | instructional

    # Persuasive angles (fully resolved)
    persuasive_angles: list[ResolvedPersuasiveAngle] = field(default_factory=list)

    # TTT gravity palette
    ttt_palette_base_gravity: Optional[TTTGravityLayer] = None
    ttt_palette_accent_layer: Optional[TTTGravityLayer] = None
    ttt_palette_intuitive_layer: Optional[TTTGravityLayer] = None

    # Guidance
    usage_notes: str = ""
    format_compatibility: list[str] = field(
        default_factory=lambda: ["video_note", "carousel", "thread"]
    )

    # Source segment (for traceability)
    source_segment_id: Optional[str] = None
    emotional_state: Optional[str] = None
    moral_foundation: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize to dict for injection into prompt payloads."""
        return asdict(self)

    def get_ttt_ceiling(self) -> str:
        """Returns the highest TTT level in the palette."""
        levels = []
        for layer in [
            self.ttt_palette_base_gravity,
            self.ttt_palette_accent_layer,
            self.ttt_palette_intuitive_layer,
        ]:
            if layer:
                # Handle compound levels like "TTT-03/TTT-05"
                for part in layer.ttt_level.split("/"):
                    part = part.strip()
                    if part.startswith("TTT-"):
                        try:
                            levels.append(int(part.split("-")[1]))
                        except (IndexError, ValueError):
                            pass
        return f"TTT-{max(levels):02d}" if levels else "TTT-01"


# ─── Registry ───────────────────────────────────────────────────────

class ArchetypeRegistry:
    """
    Deterministic router that resolves archetype metadata from 3 JSON configs.

    Loads:
        - framework_archetype_map.json  → framework binding + visual category + angle IDs
        - archetype_palettes.json       → TTT gravity tables per archetype
        - persuasive_angles.json        → full angle objects with operational instructions
    """

    def __init__(self, intelligence_library_path: str):
        self.lib_path = Path(intelligence_library_path)
        self._framework_map: dict = {}
        self._palettes: dict = {}
        self._angles: dict = {}
        self._entries_by_archetype: dict[str, list[dict]] = {}
        self._load()

    def _load(self):
        """Load all 3 JSON configs into memory."""
        # 1. Framework × Archetype map
        fam_path = self.lib_path / "framework_archetype_map.json"
        with open(fam_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._framework_map = data
        # Build index: archetype_id → list of entries
        for entry in data.get("entries", []):
            aid = entry.get("archetype_id", "")
            if aid not in self._entries_by_archetype:
                self._entries_by_archetype[aid] = []
            self._entries_by_archetype[aid].append(entry)

        # 2. Archetype palettes (TTT gravity)
        pal_path = self.lib_path / "archetype_palettes.json"
        with open(pal_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._palettes = data.get("palettes", {})

        # 3. Persuasive angles
        ang_path = self.lib_path / "persuasive_angles.json"
        with open(ang_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._angles = data.get("angles", {})

        logger.info(
            f"ArchetypeRegistry loaded: "
            f"{len(self._entries_by_archetype)} archetypes, "
            f"{len(self._palettes)} palettes, "
            f"{len(self._angles)} angles"
        )

    # ─── Core Resolution ─────────────────────────────────────────

    def resolve_archetype(
        self,
        segment: dict,
        framework_id: Optional[str] = None,
    ) -> ArchetypeMetadata:
        """
        Resolve full archetype metadata from an emotional_state_archetype_map
        segment entry.

        Args:
            segment: A dict with at minimum:
                - selected_archetype: str (archetype ID, e.g. "arch_disgusting_myth")
                - moral_foundation: str (optional, for traceability)
                - emotional_state: str (optional, for traceability)
                - voice_note_id / certificate_id: str (optional, for traceability)
            framework_id: Optional explicit framework. If not provided,
                         selects the highest-priority entry for this archetype.

        Returns:
            ArchetypeMetadata — fully resolved and ready for prompt injection.
        """
        archetype_id = segment.get("selected_archetype", "")
        if not archetype_id:
            raise ValueError("segment must contain 'selected_archetype'")

        # ── Step 1: Resolve framework binding ──
        entries = self._entries_by_archetype.get(archetype_id, [])
        if not entries:
            raise ValueError(
                f"Archetype '{archetype_id}' not found in "
                f"framework_archetype_map.json. Available: "
                f"{list(self._entries_by_archetype.keys())}"
            )

        if framework_id:
            # Filter to specific framework
            matching = [e for e in entries if e.get("framework_id") == framework_id]
            if not matching:
                logger.warning(
                    f"No entry for {archetype_id} in framework {framework_id}. "
                    f"Falling back to highest priority."
                )
                matching = entries
        else:
            matching = entries

        # Select highest priority entry
        entry = max(matching, key=lambda e: e.get("priority_level", 0))

        # ── Step 2: Resolve persuasive angles ──
        angle_ids = entry.get("persuasive_angles", [])
        resolved_angles = []
        for angle_id in angle_ids:
            angle_data = self._angles.get(angle_id)
            if angle_data:
                resolved_angles.append(
                    ResolvedPersuasiveAngle(
                        id=angle_data["id"],
                        name=angle_data["name"],
                        psychological_trigger=angle_data.get("psychological_trigger", ""),
                        operational_instruction=angle_data.get("operational_instruction", ""),
                        construction_constraint=angle_data.get("construction_constraint", ""),
                    )
                )
            else:
                logger.warning(f"Persuasive angle '{angle_id}' not found in angles.json")

        # ── Step 3: Resolve TTT palette ──
        palette = self._palettes.get(archetype_id, {})
        family = palette.get("family", "unknown")

        base_gravity = None
        accent_layer = None
        intuitive_layer = None

        if palette.get("base_gravity"):
            bg = palette["base_gravity"]
            base_gravity = TTTGravityLayer(
                ttt_level=bg["ttt_level"],
                ttt_name=bg["ttt_name"],
                focus=bg["focus"],
            )

        if palette.get("accent_layer"):
            al = palette["accent_layer"]
            accent_layer = TTTGravityLayer(
                ttt_level=al["ttt_level"],
                ttt_name=al["ttt_name"],
                focus=al["focus"],
            )

        if palette.get("intuitive_layer"):
            il = palette["intuitive_layer"]
            intuitive_layer = TTTGravityLayer(
                ttt_level=il["ttt_level"],
                ttt_name=il["ttt_name"],
                focus=il["focus"],
            )

        # ── Step 4: Determine format compatibility ──
        visual_cat = entry.get("visual_category", "sequential")
        format_compat = self._get_format_compatibility(archetype_id, visual_cat)

        # ── Step 5: Build final metadata ──
        return ArchetypeMetadata(
            archetype_id=archetype_id,
            archetype_name=entry.get("archetype_name", archetype_id),
            archetype_family=family,
            framework_id=entry.get("framework_id", ""),
            framework_name=entry.get("framework_name", ""),
            priority_level=entry.get("priority_level", 1),
            visual_category=visual_cat,
            persuasive_angles=resolved_angles,
            ttt_palette_base_gravity=base_gravity,
            ttt_palette_accent_layer=accent_layer,
            ttt_palette_intuitive_layer=intuitive_layer,
            usage_notes=entry.get("usage_notes", ""),
            format_compatibility=format_compat,
            source_segment_id=segment.get("voice_note_id") or segment.get("certificate_id"),
            emotional_state=segment.get("emotional_state"),
            moral_foundation=segment.get("moral_foundation"),
        )

    def resolve_batch(
        self,
        segments: list[dict],
        framework_id: Optional[str] = None,
    ) -> list[ArchetypeMetadata]:
        """
        Resolve archetype metadata for a batch of segments.

        Args:
            segments: List of segment dicts from emotional_state_archetype_map.json
            framework_id: Optional explicit framework for all segments.

        Returns:
            List[ArchetypeMetadata] — one per segment, in order.
        """
        results = []
        for i, segment in enumerate(segments):
            try:
                metadata = self.resolve_archetype(segment, framework_id)
                results.append(metadata)
            except ValueError as e:
                logger.error(f"Failed to resolve segment {i}: {e}")
                raise
        return results

    # ─── Lookup Helpers ──────────────────────────────────────────

    def get_archetype_ids(self) -> list[str]:
        """List all known archetype IDs from the framework map."""
        return sorted(self._entries_by_archetype.keys())

    def get_palette_ids(self) -> list[str]:
        """List all archetype IDs that have TTT palettes."""
        return sorted(self._palettes.keys())

    def get_angle_ids(self) -> list[str]:
        """List all persuasive angle IDs."""
        return sorted(self._angles.keys())

    def get_frameworks(self) -> dict[str, str]:
        """Return the framework ID → name mapping."""
        return self._framework_map.get("frameworks", {})

    def get_entries_for_framework(self, framework_id: str) -> list[dict]:
        """Return all entries for a given framework."""
        return [
            e for e in self._framework_map.get("entries", [])
            if e.get("framework_id") == framework_id
        ]

    def get_entries_for_archetype(self, archetype_id: str) -> list[dict]:
        """Return all framework entries for a given archetype."""
        return self._entries_by_archetype.get(archetype_id, [])

    def has_palette(self, archetype_id: str) -> bool:
        """Check if an archetype has a TTT palette defined."""
        return archetype_id in self._palettes

    def validate_coverage(self) -> dict:
        """
        Validate that every archetype in the framework map has a palette.
        Returns a report of missing palettes and unmatched archetypes.
        """
        map_ids = set(self._entries_by_archetype.keys())
        palette_ids = set(self._palettes.keys())

        return {
            "archetypes_in_map": len(map_ids),
            "archetypes_in_palettes": len(palette_ids),
            "missing_palettes": sorted(map_ids - palette_ids),
            "orphan_palettes": sorted(palette_ids - map_ids),
            "fully_covered": map_ids == palette_ids,
        }

    # ─── Private Helpers ─────────────────────────────────────────

    def _get_format_compatibility(
        self, archetype_id: str, visual_category: str
    ) -> list[str]:
        """
        Determine which output formats an archetype supports.
        Single-frame archetypes skip carousel. Polls skip thread.
        """
        base = ["video_note", "carousel", "thread"]

        # Tweets/memes → single format only
        if archetype_id in (
            "arch_persuasive_tweet",
            "arch_benign_violation_meme",
            "arch_incongruity_meme",
            "arch_relief_meme",
            "arch_superiority_meme",
            "arch_data_visualizer_tweet",
            "arch_thought_whisperer_tweet",
        ):
            return ["tweet"]

        # Polls → no thread (too short for long-form)
        if archetype_id in (
            "arch_poll",
            "arch_archetypical_poll",
            "arch_stereotypical_poll",
            "arch_controversial_dilemma_poll",
            "arch_would_you_rather",
        ):
            return ["video_note", "carousel"]

        # Observational humor → no thread
        if archetype_id == "arch_observational_humor":
            return ["video_note", "carousel"]

        # Single frame visuals → no carousel flow
        if visual_category == "single_frame":
            return ["video_note", "thread"]

        return base
