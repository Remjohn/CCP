"""
CCP Universal Asset ID Generator
Task 1.07 — Generates unique, human-readable identifiers for every artifact.

Format: AAAA-CCC-MM-YY-XXXX
  AAAA = Asset Type (4 chars)
  CCC  = Coach Acronym (3 chars)
  MM   = Month (01-12)
  YY   = Year (last 2 digits)
  XXXX = Random suffix (4 alphanumeric, uppercase)

Usage:
    from src.ccp.core.asset_id import AssetIDGenerator, AssetType

    gen = AssetIDGenerator(coach_acronym="NDL")
    script_id = gen.generate(AssetType.SCRIPT)
    # → "SCRP-NDL-03-26-K7M2"
"""

import random
import string
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    """All registered asset types across the CCP ecosystem."""

    # CCF — Content Production
    SCRIPT = "SCRP"           # Content script (any format)
    VISUAL_IMAGE = "VIMG"     # AI-generated visual asset
    QUOTE_CARD = "QUOT"       # Quote card / text overlay image
    MEME = "MEME"             # Meme concept + image
    CAROUSEL = "CRSL"         # Carousel slide set
    THREAD = "THRD"           # Thread / long-form text
    REEL_SCRIPT = "REEL"      # Reel / short video script
    STORY = "STRY"            # Story post content
    POLL = "POLL"             # Poll content
    ARTICLE = "ARTC"          # Long-form article
    SUGGESTION = "SUGG"       # Coach topic suggestion

    # CCF — Voice & Audio
    SACRED_AUDIO = "SAUD"     # Sacred Audio recording (coach)
    VOICE_NOTE = "VOIC"       # Voice note (client or coach)
    AUDIO_CLIP = "ACLP"       # Processed audio clip for Notion embed

    # CCF — Identity & Research
    COACH_SOUL = "SOUL"       # coach_soul.json snapshot
    RESEARCH_BRIEF = "RSBR"   # Research output document
    TRIBE_EXTRACT = "TRBE"    # Tribe distillation output
    IDEAS_JSON = "IDEA"       # ideas.json output from ccf-analyze

    # V²WS — Webinars
    WEBINAR_PACKAGE = "WBNR"  # Complete webinar package
    WEBINAR_SLIDE = "WSLD"    # Individual webinar slide
    WEBINAR_MODULE = "WMOD"   # Webinar module script

    # Tierlist
    TIERLIST = "TIER"         # Tierlist visual
    RATING = "RTNG"           # Rating visual
    REACTION_EXPLAINER = "REXP"  # Reaction explainer visual
    REACTION_IMAGE = "RIMG"   # Reaction source image

    # CBCS — Coaching
    SESSION_NOTE = "SESS"     # Session note / summary
    RITUAL = "RITL"           # Accountability ritual message
    JOURNAL_PROMPT = "JRNL"   # Journaling prompt
    PATTERN_ALERT = "PALT"    # Pattern alert notification

    # Coach Identity
    PHOTO = "PHOT"            # Personal branding photo
    LEADERSHIP_CARD = "LDRS"  # Leadership scorecard snapshot

    # Governance
    RECEIPT = "RCPT"          # Receipt Chain entry reference
    MEMORY_PROMOTION = "MPRO" # Memory promotion record
    VALIDATION_REPORT = "VRPT"  # Validation Team report
    PHASE0_ARTIFACT = "P0AF"  # Shared Phase-0 workspace artifact


class AssetID(BaseModel):
    """A parsed Universal Asset ID."""

    asset_type: AssetType
    coach_acronym: str = Field(..., min_length=3, max_length=3)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=0, le=99)
    suffix: str = Field(..., min_length=4, max_length=4)

    @property
    def full_id(self) -> str:
        return f"{self.asset_type.value}-{self.coach_acronym}-{self.month:02d}-{self.year:02d}-{self.suffix}"

    @classmethod
    def parse(cls, asset_id_str: str) -> "AssetID":
        """Parse an Asset ID string into its components.

        Example: 'SCRP-NDL-03-26-K7M2' → AssetID(...)
        """
        parts = asset_id_str.strip().upper().split("-")
        if len(parts) != 5:
            raise ValueError(
                f"Invalid Asset ID format: {asset_id_str}. "
                f"Expected AAAA-CCC-MM-YY-XXXX"
            )

        try:
            asset_type = AssetType(parts[0])
        except ValueError:
            raise ValueError(
                f"Unknown asset type code: {parts[0]}. "
                f"Valid codes: {[t.value for t in AssetType]}"
            )

        return cls(
            asset_type=asset_type,
            coach_acronym=parts[1],
            month=int(parts[2]),
            year=int(parts[3]),
            suffix=parts[4],
        )

    def __str__(self) -> str:
        return self.full_id


class AssetIDGenerator:
    """Generates unique Universal Asset IDs for a coach instance.

    Maintains an in-memory set of generated IDs for collision detection.
    Can optionally check against a Supabase registry for cross-session uniqueness.
    """

    # Characters used for the random suffix (no ambiguous chars: 0/O, 1/I/L)
    SUFFIX_CHARS = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"

    def __init__(
        self,
        coach_acronym: str,
        supabase_client: Optional[object] = None,
    ):
        self.coach_acronym = coach_acronym.upper()
        self.supabase = supabase_client
        self._generated: set[str] = set()

    def _random_suffix(self) -> str:
        """Generate a 4-character random suffix from the safe character set."""
        return "".join(random.choices(self.SUFFIX_CHARS, k=4))

    def generate(
        self,
        asset_type: AssetType,
        timestamp: Optional[datetime] = None,
    ) -> str:
        """Generate a new unique Asset ID.

        Args:
            asset_type: The type of asset being created
            timestamp: Optional override for the month/year (defaults to now UTC)

        Returns:
            A new Asset ID string (e.g. 'SCRP-NDL-03-26-K7M2')

        Raises:
            RuntimeError: If unable to generate a unique ID after 100 attempts
        """
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        month = timestamp.month
        year = timestamp.year % 100

        for _ in range(100):
            suffix = self._random_suffix()
            candidate = f"{asset_type.value}-{self.coach_acronym}-{month:02d}-{year:02d}-{suffix}"

            if candidate not in self._generated:
                # Check Supabase if configured
                if self.supabase and self._exists_in_registry(candidate):
                    continue

                self._generated.add(candidate)
                return candidate

        raise RuntimeError(
            f"Failed to generate unique Asset ID after 100 attempts "
            f"for type={asset_type.value}, coach={self.coach_acronym}"
        )

    def generate_batch(
        self,
        asset_type: AssetType,
        count: int,
        timestamp: Optional[datetime] = None,
    ) -> list[str]:
        """Generate multiple unique Asset IDs in one call.

        Args:
            asset_type: The type of asset
            count: Number of IDs to generate
            timestamp: Optional override for month/year

        Returns:
            List of unique Asset ID strings
        """
        return [self.generate(asset_type, timestamp) for _ in range(count)]

    def register(self, asset_id: str) -> None:
        """Register an externally-created Asset ID to prevent collisions."""
        self._generated.add(asset_id.upper())

    def _exists_in_registry(self, asset_id: str) -> bool:
        """Check if an Asset ID already exists in the Supabase registry."""
        try:
            result = (
                self.supabase.table("asset_registry")
                .select("asset_id")
                .eq("asset_id", asset_id)
                .execute()
            )
            return len(result.data) > 0
        except Exception:
            # If Supabase check fails, rely on in-memory check only
            return False

    def save_to_registry(self, asset_id: str, metadata: Optional[dict] = None) -> None:
        """Persist an Asset ID to the Supabase asset_registry table."""
        if not self.supabase:
            return

        parsed = AssetID.parse(asset_id)
        try:
            self.supabase.table("asset_registry").insert(
                {
                    "asset_id": asset_id,
                    "asset_type": parsed.asset_type.value,
                    "coach_acronym": parsed.coach_acronym,
                    "month": parsed.month,
                    "year": parsed.year,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    **(metadata or {}),
                }
            ).execute()
        except Exception as e:
            import sys
            print(
                f"[AssetID] Registry save failed for {asset_id}: {e}",
                file=sys.stderr,
            )

    @property
    def generated_count(self) -> int:
        """Number of IDs generated in this session."""
        return len(self._generated)
