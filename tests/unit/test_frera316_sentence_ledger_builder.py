"""Unit tests for SentenceLedgerBuilder — FR-ERA3-16."""
from src.ccp.services.archetype_container_runtime import SentenceLedgerBuilder


class TestSentenceIdsAndOffsetsStable:
    """test_sentence_ids_and_offsets_are_stable_for_same_transcript"""

    def test_same_transcript_produces_same_ids(self):
        transcript = "Most coaches copy the market. They are scared to say who they disagree with. That is the real problem."
        result_a = SentenceLedgerBuilder.build(transcript)
        result_b = SentenceLedgerBuilder.build(transcript)

        assert len(result_a) == len(result_b)
        for a, b in zip(result_a, result_b):
            assert a.sentence_id == b.sentence_id
            assert a.start_offset == b.start_offset
            assert a.end_offset == b.end_offset

    def test_sentence_ids_are_sequential(self):
        transcript = "First sentence. Second sentence. Third sentence."
        result = SentenceLedgerBuilder.build(transcript)
        assert [s.sentence_id for s in result] == ["S1", "S2", "S3"]


class TestSentenceSplitterPreservesExactText:
    """test_sentence_splitter_preserves_exact_text_for_rejection_quotes"""

    def test_exact_text_preserved(self):
        transcript = "Every business should just focus on authenticity. At the end of the day we all need to be ourselves."
        result = SentenceLedgerBuilder.build(transcript)
        for sentence in result:
            assert sentence.text in transcript

    def test_offsets_match_text(self):
        transcript = "First. Second. Third."
        result = SentenceLedgerBuilder.build(transcript)
        for sentence in result:
            extracted = transcript[sentence.start_offset:sentence.end_offset]
            assert extracted == sentence.text


class TestEmptyTranscriptInvalid:
    """test_sentence_ledger_marks_empty_or_whitespace_only_transcript_invalid"""

    def test_empty_string_returns_empty(self):
        assert SentenceLedgerBuilder.build("") == []

    def test_whitespace_only_returns_empty(self):
        assert SentenceLedgerBuilder.build("   ") == []
