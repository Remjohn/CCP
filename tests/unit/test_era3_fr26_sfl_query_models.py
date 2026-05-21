from __future__ import annotations

from pathlib import Path
import sys

from pydantic import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.ccp.models.sfl_query_models import (
    DeliverySurfaceKind,
    FunctionProfileAssemblyRequest,
    ProfileConflictRecord,
    SFLAssemblyStatus,
    SFLQueryMode,
    SFLVersionStamp,
    SubliminalFunctionQueryRequest,
    SubliminalFunctionStackPacket,
)


def test_query_request_requires_matching_target_for_mode() -> None:
    try:
        SubliminalFunctionQueryRequest(query_mode=SFLQueryMode.BY_FAMILY)
    except ValidationError as exc:
        assert "Missing required target for query_mode=by_family" in str(exc)
    else:
        raise AssertionError("Expected query request validation to fail without family_id")


def test_stack_packet_requires_valid_sfl_function_ids() -> None:
    try:
        SubliminalFunctionStackPacket(
            packet_id="pkt-1",
            delivery_surface=DeliverySurfaceKind.TELEGRAM,
            status=SFLAssemblyStatus.RESOLVED,
            active_family_ids=["SFL-FAM-001"],
            active_function_ids=["BAD-FN-001"],
            version_stamp=SFLVersionStamp(
                manifest_version="1.0",
                manifest_hash="12345678",
                registry_hash="87654321",
            ),
        )
    except ValidationError as exc:
        assert "Invalid function reference" in str(exc)
    else:
        raise AssertionError("Expected stack packet validation to fail for noncanonical function id")


def test_profile_conflict_record_restricts_scope_values() -> None:
    try:
        ProfileConflictRecord(
            conflict_id="SFL-CF-001",
            higher_priority_evidence_ref="SFL-XW-SF-001",
            lower_priority_evidence_ref="SFL-XW-AR-001",
            conflict_scope="bad_scope",
            affected_function_ids=["SFL-FN-004"],
            resolution="review_required",
            rationale="bad",
        )
    except ValidationError as exc:
        assert "conflict_scope" in str(exc)
    else:
        raise AssertionError("Expected conflict scope validation to fail")


def test_assembly_request_rejects_noncanonical_override_ids() -> None:
    try:
        FunctionProfileAssemblyRequest(
            delivery_surface=DeliverySurfaceKind.TELEGRAM,
            explicit_function_ids=["fn-1"],
            explicit_family_ids=["fam-1"],
        )
    except ValidationError as exc:
        assert "Invalid explicit function id" in str(exc) or "Invalid explicit family id" in str(exc)
    else:
        raise AssertionError("Expected assembly request validation to fail for noncanonical override ids")
