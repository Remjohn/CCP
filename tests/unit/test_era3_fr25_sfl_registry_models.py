from __future__ import annotations

from pydantic import ValidationError

from src.ccp.models.sfl_registry_models import (
    FunctionFamilyCompressionRuleRecord,
    SourceDocumentRef,
    SubliminalFunctionDefinitionRecord,
    SubliminalFunctionFamilyRecord,
    SurfaceConstraintProfileRecord,
)


def _doc_ref() -> list[SourceDocumentRef]:
    return [SourceDocumentRef(path="lab/subliminal_function_layer_for_ccp_v_1.md", note="test fixture")]


def test_family_record_rejects_empty_related_raw_terms() -> None:
    try:
        SubliminalFunctionFamilyRecord.model_validate(
            {
                "artifact_id": "SFL-FAM-999",
                "artifact_class": "canonical_function_family",
                "canonical_name": "Test Family",
                "family_kind": "identity_signaling",
                "definition": "A sufficiently long family definition for validation.",
                "purpose": "A sufficiently long purpose description for validation.",
                "positive_space_role": "A sufficiently long positive role description for validation.",
                "negative_space_boundary": "A sufficiently long negative boundary description for validation.",
                "anti_bloat_guidance": "A sufficiently long anti-bloat guidance description for validation.",
                "related_raw_terms": [],
                "source_documents": [doc.model_dump() for doc in _doc_ref()],
            }
        )
    except ValidationError:
        return
    raise AssertionError("expected ValidationError for empty related_raw_terms")


def test_function_definition_rejects_missing_family_id() -> None:
    try:
        SubliminalFunctionDefinitionRecord.model_validate(
            {
                "artifact_id": "SFL-FN-999",
                "artifact_class": "function_definition",
                "canonical_name": "Test Function",
                "polarity": "positive",
                "definition": "A sufficiently long function definition for validation.",
                "positive_operation": "A sufficiently long positive operation description for validation.",
                "negative_operation": "A sufficiently long negative operation description for validation.",
                "intended_effects": [{"effect_key": "memory_trace", "description": "test effect"}],
                "alignment_rules": [
                    {
                        "allowed_when": "long enough allowed rule",
                        "disallowed_when": "long enough disallowed rule",
                        "downgrade_behavior": "long enough downgrade behavior",
                    }
                ],
                "source_documents": [doc.model_dump() for doc in _doc_ref()],
            }
        )
    except ValidationError:
        return
    raise AssertionError("expected ValidationError for missing family_id")


def test_compression_rule_rejects_empty_raw_term_list() -> None:
    try:
        FunctionFamilyCompressionRuleRecord.model_validate(
            {
                "artifact_id": "SFL-CR-999",
                "artifact_class": "compression_rule",
                "canonical_family_id": "SFL-FAM-001",
                "raw_terms": [],
                "compression_rationale": "A sufficiently long compression rationale for validation.",
                "source_documents": [doc.model_dump() for doc in _doc_ref()],
            }
        )
    except ValidationError:
        return
    raise AssertionError("expected ValidationError for empty raw_terms")


def test_surface_constraint_profile_requires_known_surface_kind() -> None:
    try:
        SurfaceConstraintProfileRecord.model_validate(
            {
                "artifact_id": "SFL-XW-SF-999",
                "artifact_class": "crosswalk",
                "surface": "discord",
                "preferred_family_ids": [],
                "discouraged_family_ids": [],
                "hard_constraints": [],
                "rationale": "A sufficiently long rationale for validation in the test fixture.",
                "source_documents": [doc.model_dump() for doc in _doc_ref()],
            }
        )
    except ValidationError:
        return
    raise AssertionError("expected ValidationError for unknown surface kind")
