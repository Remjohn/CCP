"""
CCP Pydantic Models — Genesis Clearance Certificate (DEP-ENG-052)
FR-GA Task 3 — Immutable proof that production foundation is authenticated.

The Genesis Clearance Certificate is the gate object that must exist
before any FR1+ spec can execute. Without it, the production pipeline
is locked.

Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Genesis Clearance Certificate
Stores: stage_verdicts, provisional_gaps[], receipt_chain_root, is_valid
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.ccp.models.guardian_models import GenesisVerdict


class GenesisClearanceCertificate(BaseModel):
    """Immutable proof that the Pre-Production Intelligence Layer is authenticated.

    DEP-ID: DEP-ENG-052
    Producing FR: FR-GA (Guardian Agent)
    Consuming FRs: FR1 (prerequisite gate — code-level lock)

    AC1: Without this certificate, triggering FR1's ccf-init returns
    GENESIS_CLEARANCE_REQUIRED — code-level gate.
    """

    certificate_id: str = Field(
        ...,
        description="Unique certificate identifier (UUID format)",
    )
    coach_id: str = Field(
        ...,
        description="Coach Person ID (CCC-0000)",
    )
    coach_acronym: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="3-letter coach acronym",
    )
    issued_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp of certificate issuance",
    )
    stage_verdicts: dict[str, GenesisVerdict] = Field(
        ...,
        description=(
            "Verdict for each FR0x stage. Keys: FR0A, FR0B, FR0C, FR0D, FR0E. "
            "All must be AUTHENTICATED or PROVISIONAL for certificate to be valid."
        ),
    )
    provisional_gaps: list[str] = Field(
        default_factory=list,
        description="Specific gaps flagged for any PROVISIONAL verdicts",
    )
    receipt_chain_root: str = Field(
        ...,
        description=(
            "SHA-256 hash linking to the genesis receipt chain root. "
            "Provides cryptographic traceability to every stage execution."
        ),
    )
    is_valid: bool = Field(
        ...,
        description="True only if no FAILED verdicts exist across all stages",
    )
    certificate_hash: str = Field(
        default="",
        description="SHA-256 integrity hash of the certificate content (auto-generated)",
    )
    genesis_duration_ms: float = Field(
        default=0.0,
        description="Total Genesis Mode execution duration in milliseconds",
    )
    authentic_multiplier: Optional[float] = Field(
        default=None,
        description=(
            "Coach-specific LIWC-22 authenticity floor adjustment. "
            "Extracted during Genesis. Overrides the generic 7/10 floor."
        ),
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional structured data (interview summary, stage timings)",
    )

    def model_post_init(self, __context: Any) -> None:
        """Generate certificate_hash from content after initialization."""
        if not self.certificate_hash:
            content = json.dumps(
                {
                    "certificate_id": self.certificate_id,
                    "coach_id": self.coach_id,
                    "stage_verdicts": {
                        k: v.value for k, v in self.stage_verdicts.items()
                    },
                    "receipt_chain_root": self.receipt_chain_root,
                    "is_valid": self.is_valid,
                },
                sort_keys=True,
            )
            self.certificate_hash = hashlib.sha256(content.encode()).hexdigest()

    def has_provisional_stages(self) -> bool:
        """Check if any stage has a PROVISIONAL verdict."""
        return any(
            v == GenesisVerdict.PROVISIONAL for v in self.stage_verdicts.values()
        )

    def get_authenticated_stages(self) -> list[str]:
        """Return list of stage names with AUTHENTICATED verdict."""
        return [
            k for k, v in self.stage_verdicts.items()
            if v == GenesisVerdict.AUTHENTICATED
        ]

    def get_provisional_stages(self) -> list[str]:
        """Return list of stage names with PROVISIONAL verdict."""
        return [
            k for k, v in self.stage_verdicts.items()
            if v == GenesisVerdict.PROVISIONAL
        ]


class CertificateOverride(BaseModel):
    """Manual operator override when Genesis Certificate is pending.

    Spec reference: FR_GA_Guardian_Agent_Tech_Spec.md §Backward Compatibility Fallback
    """

    coach_id: str = Field(..., description="Coach Person ID")
    override_reason: str = Field(
        ...,
        description="Documented reason for the override",
    )
    overridden_by: str = Field(
        ...,
        description="Operator ID who issued the override",
    )
    overridden_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 UTC timestamp",
    )
    genesis_certificate_override: bool = Field(
        default=True,
        description="Always True for override records (spec requirement)",
    )
