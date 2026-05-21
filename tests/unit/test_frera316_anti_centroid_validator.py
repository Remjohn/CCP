"""Unit tests for AntiCentroidValidator — FR-ERA3-16.
NOT reusing semantic_affinity_guard.py (AC6)."""
from src.ccp.services.archetype_container_runtime import (
    AntiCentroidValidator,
    SentenceLedgerBuilder,
    SimilarityBand,
)


class TestGenericConsensusSentencesReturnTerminal:
    """test_generic_consensus_sentences_return_terminal_similarity_band"""

    def test_abstract_consensus_is_terminal(self):
        transcript = "Every business should just focus on authenticity. At the end of the day we all need to be ourselves."
        sentences = SentenceLedgerBuilder.build(transcript)
        validator = AntiCentroidValidator()
        audited = validator.validate(sentences)

        terminal_count = sum(1 for s in audited if s.similarity_band == SimilarityBand.TERMINAL)
        assert terminal_count >= 1, "At least one generic consensus sentence must be terminal."

    def test_terminal_has_similarity_above_threshold(self):
        transcript = "Every business should just focus on authenticity."
        sentences = SentenceLedgerBuilder.build(transcript)
        validator = AntiCentroidValidator()
        audited = validator.validate(sentences)

        for s in audited:
            if s.similarity_band == SimilarityBand.TERMINAL:
                assert s.similarity_score >= 0.75


class TestSpecificNamedExampleReducesScore:
    """test_specific_named_example_reduces_similarity_score_below_rejection_threshold"""

    def test_named_proof_lowers_score(self):
        transcript = "When Sarah lost 40 clients in January 2024, she rebuilt her funnel using 3 specific cold email templates."
        sentences = SentenceLedgerBuilder.build(transcript)
        validator = AntiCentroidValidator()
        audited = validator.validate(sentences)

        for s in audited:
            assert s.similarity_band != SimilarityBand.TERMINAL, f"Sentence with specific names/numbers should not be terminal: {s.text}"


class TestRejectionPayloadContainsExactIds:
    """test_rejection_payload_contains_exact_sentence_ids_and_coaching_fix"""

    def test_failing_sentences_have_ids(self):
        transcript = "Every business should just focus on authenticity. Success comes from growth mindset."
        sentences = SentenceLedgerBuilder.build(transcript)
        validator = AntiCentroidValidator()
        audited = validator.validate(sentences)

        failing = [s for s in audited if s.failed]
        assert len(failing) >= 1
        for s in failing:
            assert s.sentence_id.startswith("S")
            assert len(s.collapse_reason) > 0
